from typing import Callable


class String:
    """Wrapper for `str` type, make it more functional style and adding useful parser for nlp processing."""

    def __init__(self, string):
        self._raw = string
        self._value = string

    def __getattr__(self, name: str):

        if hasattr(self._value, name):
            func = getattr(self._value, name, None)
            if callable(func):
                return self.apply(func)

        raise AttributeError(
            f"`{self.__class__.__name__}` object has no attribute `{name}`"
        )

    def apply(self, func: Callable[[str], str]) -> "String":
        self._value = func(self._value)

        return self

    def to_str(self):
        """Convert back to `str`."""

        return self._value

    def __str__(self):

        return self.to_str()

    def __repr__(self):

        return self.to_str()


def split_and_join(text: str, splitter: str = "", joiner: str = "") -> str:
    """Split string first, then join back to a new string by specified delimiter."""

    return joiner.join(text.split(splitter or None))


def halfwidth(text: str) -> str:
    """Convert the string to halfwidth.

    full-width characters' unicodes range from 65281 to 65374 (0xFF01 - 0xFF5E in hex)
    half-width characters' unicodes range from 33 to 126 (0x21 - 0x7E in hex)
    `space` in full-width: 12288(0x3000), in half-width: 32(0x20)
    since the unicode difference is fixed between
    full- and half-width forms of single character,
    convert the character to half-width by numeric shifting,
    and handle `space` as a special case
    """
    rstring = ""
    for char in text:
        code = ord(char)
        if code == 0x3000:
            code = 0x0020
        else:
            code -= 0xFEE0
        if code < 0x0020 or code > 0x7E:  # fallback check
            rstring += char
        else:
            rstring += chr(code)
    return rstring
