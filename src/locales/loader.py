import gettext
from functools import lru_cache

from fastapi import Header

SUPPORTED_LANGUAGES = ["fa", "en"]
DEFAULT_LANGUAGE = "en"


@lru_cache
def get_translation(lang: str):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    return gettext.translation(
        domain="messages", localedir="src/locales", languages=[lang]
    )


def translate(lang: str, msgid: str) -> str:
    t = get_translation(lang)
    return t.gettext(msgid)


def get_language(accept_language: str | None = Header(None)) -> str:
    if not accept_language or accept_language not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE
    return accept_language.lower()
