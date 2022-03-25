from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def formatted(self):
        return self.value.replace('_', ' ')
