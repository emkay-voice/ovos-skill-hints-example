# Hints when nobody understood

Say something no skill understands, with a word it knows in it –
**"um, the clock thing"** – and it suggests the sentence you may have meant:
*"I didn't get that. Did you mean: “what time is it”?"* – in all twelve of
[Emkay](https://emkay.ai)'s languages.

**👉 The friendly guide: <https://dev.emkay.ai>**

## What it shows

- **A fallback skill, no intents:** when no skill understood a sentence,
  OpenVoiceOS asks the fallback skills one by one, the lowest priority number
  first. `@fallback_handler(priority=PRIORITY)` puts `handle_fallback` in
  that line.
- **can_answer:** OpenVoiceOS first asks every fallback whether it can
  answer; a `FallbackSkill` must have it, or it won't load.
- **True or False:** return `True` when you answered; `False` lets the next
  fallback try – in the end the one that says "I don't understand" (priority
  100).
- **Your own words per language:** `locale/<language>/hints.list`,
  `word, word | the sentence to suggest`.

## Try changing

- `hints.list` – sentences your own skills understand;
- `PRIORITY` – lower is asked earlier;
- ask back instead (`self.ask_yesno(...)`) and, on yes, say the sentence for
  the user: `self.bus.emit(message.forward("recognizer_loop:utterance",
  {"utterances": [hint]}))`.

## A working skill, and a template

This is a complete OpenVoiceOS skill – install it and it works – and an
example to start your own from: *Use this template* on GitHub, or
*Emkay: New skill* in VS Code ([Emkay Dev](https://dev.emkay.ai)), which
gives it your own names. Made for [Emkay](https://emkay.ai), it runs on any
OpenVoiceOS.

## Try it

- **Emkay Dev (VS Code):** *Emkay: Run the skill in Emkay* (Ctrl+Alt+E) opens
  Emkay next to your code and loads the skill; type under Emkay to talk to it.
  Every save loads it again. *Emkay: Test the skill* sends the golden
  utterances and shows ✓ / ✗ in the Testing view. Emkay's menu →
  *Guardian* → *What's happening?* shows which skill took a sentence, and why.
- **ovos-tui-client (Codespaces, Dev Container):** run `ovos-tui` in the
  terminal, type to talk, `Ctrl+P` → *Test* runs the same golden utterances
  against a full OpenVoiceOS.
- **pytest:** `pytest -q` – no OpenVoiceOS needed.

When you make a repository from this template ("Use this template"), a
small workflow renames the skill after your repository and then removes
itself.

## Show it, on your own Emkay, and into the store

To show it in [See my skill](https://dev.emkay.ai/#gallery) on dev.emkay.ai –
ready or not – add the topic `emkay-skill` to the repository (the ⚙ next to
*About*). Remove the topic, or make the repository private, to take it away.

*Emkay: Send to my Emkay* shows a QR code that installs this skill from
GitHub on the Emkay you scan it with. To get it into the
[Emkay store](https://store.emkay.ai): topics `ovos` and `openvoiceos` on the
repository, a release on GitHub (`publish.yml` puts it on PyPI), and the
store's nightly test does the rest – <https://dev.emkay.ai/#store>.

More on writing skills:
[the OpenVoiceOS technical manual](https://openvoiceos.github.io/ovos-technical-manual/).
