from diskcache import Cache
from pathlib import Path
from functools import wraps
from pickle import dumps, loads
from itertools import chain
from inspect import iscoroutinefunction


class _CacherDecorator:
    def __init__(self, base, directory: Path, *functions):
        self._path = base / directory
        self._cache = Cache(directory=str(self._path))
        self._functions = functions

    def __call__(self, cls):
        for function in self._functions:
            setattr(cls, function, self._create_call(getattr(cls, function)))

        return cls

    @classmethod
    def _func_call_key(cls, function, args, kwargs):
        return f'{function.__name__}({",".join(chain(map(repr, args), map(lambda key, value: f"{repr(key)}={repr(value)}", kwargs.items())))})'

    def _create_async_call(self, function):
        @wraps(function)
        async def _cached_call(*args, **kwargs):
            with Cache(self._cache.directory) as reference:
                call_key = self._func_call_key(function, args, kwargs)
                if call_key in reference:
                    return loads(reference.get(call_key))
                else:
                    result = await function(*args, **kwargs)
                    reference.set(call_key, dumps(result))
                    return result

        return _cached_call

    def _create_cached_call(self, function):
        @wraps(function)
        def _cached_call(*args, **kwargs):
            with Cache(self._cache.directory) as reference:
                call_key = self._func_call_key(function, args, kwargs)
                if call_key in reference:
                    return loads(reference.get(call_key))
                else:
                    result = function(*args, **kwargs)
                    reference.set(call_key, dumps(result))
                    return result

        return _cached_call

    def _create_call(self, function):
        if iscoroutinefunction(function):
            return self._create_async_call(function)
        else:
            return self._create_cached_call(function)


class Cacher:
    base = Path('cache')

    @classmethod
    def cache_calls(cls, *args, **kwargs):
        return _CacherDecorator(cls.base, *args, **kwargs)
