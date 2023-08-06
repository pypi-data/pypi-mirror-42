from .helpers_py3 import types as py3_types
from .helpers_ts import types as ts_types

def type_helper(scope, *args) -> str:
    language: str = args[0]
    typevar: str = args[1]

    if language == 'py':
        return py3_types.get(typevar, typevar)
    elif language == 'ts':
        return ts_types.get(typevar, typevar)

    raise Exception(f"Unknown language `{language}` to resolve `{typevar}` for.")
