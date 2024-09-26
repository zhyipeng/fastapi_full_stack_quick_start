from enum import Enum
from typing import NoReturn


class BusinessException(Exception):
    def __init__(self, error_code: int, error_message: str):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class Errors(Enum):
    Success = 0, ''
    UnknownError = 1, 'Unknow error'

    def raise_exc(self, error_msg: str | None = None) -> NoReturn:
        raise BusinessException(self.value[0], error_msg or self.value[1])
