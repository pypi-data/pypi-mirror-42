import os
from functools import wraps
from typing import Dict


def qualname(obj, default: str = "<unknown>"):
    module = getattr(obj, "__module__", default)
    name = getattr(obj, "__qualname__", default)

    return f"{module}.{name}"


def deprecated(cls_or_fn, replaced_by=None):
    """A Wrapper to mark any implementations(classes or functions) as deprecated"""

    def wrapper(_callable):
        @wraps(_callable)
        def inner(*args, **kwargs):
            replacement = (
                f", and will be replaced by: `{qualname(replaced_by)}`"
                if replaced_by
                else ""
            )

            print(f"\n[WARNING] `{qualname(_callable)}` is deprecated {replacement}\n")

            return _callable(*args, **kwargs)

        return inner

    if cls_or_fn:
        return wrapper(cls_or_fn)

    else:
        return wrapper


class SimpleTemplate:

    __slots__ = ("_template", "_default_params")

    @classmethod
    def join_from(
        cls,
        other: "SimpleTemplate",
        template: str,
        sep: str = os.path.sep,
        **defaut_params: str,
    ) -> "SimpleTemplate":

        return cls(
            sep.join([other.template, template]),
            **dict(**other.default_params, **defaut_params),
        )

    def __init__(self, template: str, **default_params):

        self._template = template
        self._default_params = default_params

    @property
    def template(self) -> str:
        return self._template

    @property
    def default_params(self) -> Dict:
        return self._default_params

    def __call__(self, **params: str):
        populates = {k: params.get(k, v) for k, v in self.default_params.items()}
        return self.template.format(**populates)

    def to_str(self) -> str:
        return str(self)

    def __str__(self):
        return self.template.format(**self.default_params)

    def __repr__(self):
        return f"<ST: {str(self)}>"
