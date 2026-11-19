"""Quick checks that run without OpenVoiceOS running: `pytest`.

Talking to the skill is the real test - in Emkay (Emkay: Test the skill)
or with ovos-tui-client against an OVOS - but these catch the usual slips
early: a language missing a file, or an intent with no answer.
"""
import json
import sys
from pathlib import Path

from ovos_bus_client.message import Message
from ovos_utils.fakebus import FakeBus

ROOT = Path(__file__).parent.parent
PACKAGE = ROOT / "ovos_skill_hints_example"
sys.path.insert(0, str(ROOT))
import ovos_skill_hints_example as pkg  # noqa: E402

SKILL_ID = "ovos-skill-hints-example.emkay-voice"
LANGS = sorted(p.name for p in (PACKAGE / "locale").iterdir() if p.is_dir())


def test_every_language_has_the_same_files():
    first = sorted(f.name for f in (PACKAGE / "locale" / LANGS[0]).iterdir())
    for lang in LANGS[1:]:
        assert sorted(f.name for f in (PACKAGE / "locale" / lang).iterdir()) == first, lang


def test_golden_utterances_are_for_this_skill():
    for f in (ROOT / "test" / "end2end").glob("golden_utterances_*.jsonl"):
        for line in f.read_text().splitlines():
            if line.strip():
                assert json.loads(line)["skill_id"] == SKILL_ID, f.name


def test_the_skill_can_be_made():
    # OpenVoiceOS refuses to load a FallbackSkill without can_answer
    assert not getattr(pkg.HintsSkill, "__abstractmethods__", None)
def test_a_hint_by_a_word_in_the_sentence():
    hints = [(["clock", "time"], "what time is it"), (["joke"], "tell me a joke")]
    assert pkg.find_hint("um the clock thing", hints) == "what time is it"
    assert pkg.find_hint("a JOKE please", hints) == "tell me a joke"
    assert pkg.find_hint("blorp the zibble", hints) is None
    assert pkg.find_hint("o'clockwork", hints) is None     # a whole word, not part of one


def test_every_language_has_hints_and_says_the_sentence():
    for lang in LANGS:
        loc = PACKAGE / "locale" / lang
        rows = [l for l in (loc / "hints.list").read_text().splitlines() if l.strip()]
        assert len(rows) >= 4 and all("|" in r for r in rows), lang
        assert "{sentence}" in (loc / "did_you_mean.dialog").read_text(), lang
