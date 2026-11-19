"""Hints when nobody understood: "um, the clock thing" -> "Did you mean: what time is it?"

A fallback skill: there are no intents. When no skill understood what you
said, OpenVoiceOS first asks every fallback skill whether it can answer
(can_answer), then lets them try one by one, lowest priority number first
(PRIORITY). This one looks for a word it knows in the sentence
(locale/<language>/hints.list, one line each:  word, word | the sentence to
suggest) and suggests that sentence. If it finds none it returns False, and
the next fallback gets its turn – in the end the one that says "I don't
understand".

Try changing: the words and sentences in hints.list (sentences that your
own skills understand), PRIORITY, or ask back instead ("Shall I?") and say
the sentence for the user.
"""
from ovos_bus_client.session import SessionManager
from ovos_workshop.decorators import fallback_handler
from ovos_workshop.skills.fallback import FallbackSkill

PRIORITY = 80   # 0-100: lower is asked first; "I don't understand" is 100


def words(text):
    return " ".join("".join(c if c.isalnum() else " " for c in (text or "").lower()).split())


def find_hint(sentence, hints):
    """The sentence to suggest for the first word of `hints` that is in `sentence`, or None."""
    said = f" {words(sentence)} "
    for keys, suggestion in hints:
        if any(f" {words(k)} " in said for k in keys):
            return suggestion
    return None


class HintsSkill(FallbackSkill):

    def hints(self, lang):
        """[([words], sentence)] from hints.list in that language."""
        path = self.find_resource("hints.list", lang=lang)
        out = []
        for line in open(path, encoding="utf-8") if path else []:
            if "|" in line and not line.startswith("#"):
                keys, suggestion = line.split("|", 1)
                out.append(([k.strip() for k in keys.split(",") if k.strip()], suggestion.strip()))
        return out

    def hint_for(self, message):
        lang = SessionManager.get(message).lang or self.lang
        hints = self.hints(lang)
        for utterance in message.data.get("utterances") or [message.data.get("utterance", "")]:
            hint = find_hint(utterance, hints)
            if hint:
                return hint
        return None

    def can_answer(self, message):
        """Asked before the fallback runs: can we say something useful to this?"""
        return self.hint_for(message) is not None

    @fallback_handler(priority=PRIORITY)
    def handle_fallback(self, message):
        """Nobody understood: True when we said something, False to let the next fallback try."""
        hint = self.hint_for(message)
        if not hint:
            return False
        self.speak_dialog("did_you_mean", {"sentence": hint})
        return True
