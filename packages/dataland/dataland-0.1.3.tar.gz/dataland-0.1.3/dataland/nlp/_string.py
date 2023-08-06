from functools import wraps
from typing import Any, AnyStr, Callable

import regex


class String:
    """Wrapper for `str` type, make it more functional style and adding useful parser for nlp processing."""

    def __init__(self, string):
        self._raw = string
        self._value = string

    def _wrap(
        self, func: Callable[[Any], str], *args, **kwargs
    ) -> Callable[[Any], AnyStr]:
        @wraps(func)
        def _inner(*args, **kwargs):
            return self.apply(func, *args, **kwargs)

        return _inner

    def __getattr__(self, name: str, *args, **kwargs):

        func = getattr(str, name, None)

        if callable(func):

            return self._wrap(func, *args, **kwargs)

        raise AttributeError(f"`String` object has no attribute `{name}`")

    def replace(self, old: str, new: str) -> "String":
        self._value = regex.sub(old, new, self._value)

        return self

    def apply(self, func: Callable[[str], str], *args, **kwargs) -> AnyStr:
        r = func(self._value, *args, **kwargs)

        # TODO: manage side effect
        if isinstance(r, str):
            self._value = r
            return self
        else:
            return r

    def to_str(self):
        """Convert back to `str`."""

        return self._value

    def __str__(self):

        return self.to_str()

    def __repr__(self):

        return f"<Str: {self.to_str()}>"
