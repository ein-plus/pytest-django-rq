import inspect
from functools import wraps
from typing import Sequence, Tuple, Callable

_sentinel = object()


def memorize(key_params: Sequence[str] = ()):
    memory = {}

    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = extract_args(func, key_params, *args, **kwargs)
            result = memory.get(key, _sentinel)
            if result is _sentinel:
                # not in memory, set it
                result = memory[key] = func(*args, **kwargs)
            return result

        return wrapper

    return deco


def extract_args(f: Callable, key_params: Sequence[str], *args, **kwargs) -> Tuple[str]:
    """Return a tuple with arguments passed through."""
    sig = inspect.signature(f)
    ba = sig.bind(*args, **kwargs)
    return tuple(
        ba.arguments.get(name, sig.parameters[name].default) for name in key_params
    )
