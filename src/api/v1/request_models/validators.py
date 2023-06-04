import re

from pydantic import validator

VALID_FIRST_LAST_NAME = r'^[А-ЯЁ][а-яё]*([-][А-ЯЁа-яё][а-яё]+)*$'
F_L_NAME_TEXT_ERROR = (
    'В поле `{field_name}` может быть использована только кириллица '
    'или `-`. Поле `{field_name}` должно начинаться с заглавной буквы.'
)

VALID_USERNAME = r'^[A-z][A-z0-9]+$'
USERNAME_TEXT_ERROR = ('В поле `{field_name}` могут быть использованы только '
                       'буквы английского алфавита.')

VALID_DEPART_POSITION = r'^[А-ЯЁ][А-яЁё]*([- ][а-яё]+)*$'
DEPART_POSITION_TEXT_ERROR = (
    'В поле `{field_name}` может быть использована только кириллица, '
    'пробел или `-`. Поле `{field_name}` должно начинаться с заглавной'
    ' буквы.'
)


def match_regex_pattern(
    value: str, pattern: str, error_text: str, field_name: str
) -> str:
    if not re.compile(pattern).match(value):
        message = error_text.format(field_name=field_name)
        raise ValueError(message)
    return value


def first_and_last_name_validator(field_name: str) -> str:
    return validator(field_name, allow_reuse=True)(
        lambda v: match_regex_pattern(
            v, VALID_FIRST_LAST_NAME, F_L_NAME_TEXT_ERROR, field_name
        )
    )


def username_validator(field_name: str) -> str:
    return validator(field_name, allow_reuse=True)(
        lambda v: match_regex_pattern(
            v, VALID_USERNAME, USERNAME_TEXT_ERROR, field_name
        )
    )


def department_position_validator(field_name: str):
    return validator(field_name, allow_reuse=True)(
        lambda v: match_regex_pattern(
            v, VALID_DEPART_POSITION,
            DEPART_POSITION_TEXT_ERROR, field_name
        )
    )
