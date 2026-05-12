import gettext
from functools import lru_cache
from pathlib import Path

from fastapi import Header

from configs import get_settings


@lru_cache
def get_translation(lang: str):

    if lang not in get_settings().SUPPORTED_LANGUAGES:
        lang = get_settings().DEFAULT_LANGUAGE

    return gettext.translation(
        domain="messages",
        localedir=Path(get_settings().LANGUAGES_LOCALES_DIR),
        languages=[lang],
    )


def translate(lang: str, msgid: str) -> str:
    t = get_translation(lang)
    return t.gettext(msgid)


def get_language(accept_language: str | None = Header(None)) -> str:
    if (
        not accept_language
        or accept_language not in get_settings().SUPPORTED_LANGUAGES
    ):
        return get_settings().DEFAULT_LANGUAGE
    return accept_language.lower()
