import inspect
from functools import wraps
from typing import Sequence, Tuple

_sentinel = object()


def memorize(key_params: Sequence[str] = ()):
    memory = {}

    def deco(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            ba = sig.bind(*args, **kwargs)
            key = extract_args(sig, ba, key_params)
            result = memory.get(key, _sentinel)
            if result is _sentinel:
                # not in memory, set it
                result = memory[key] = func(*args, **kwargs)
            return result

        return wrapper

    return deco


def extract_args(
    sig: inspect.Signature, ba: inspect.BoundArguments, key_params: Sequence[str]
) -> Tuple[str]:
    """Return a tuple with arguments passed through.

    >>> def f(host='localhost', port=8888, retry=3):
    ...    pass
    >>> sig = inspect.signature(f)
    >>> ba = sig.bind(port=8000)
    >>> extract_args(sig, ba, ('host', 'port'))
    ('localhost', 8000)
    """
    return tuple(
        ba.arguments.get(name, sig.parameters[name].default) for name in key_params
    )
