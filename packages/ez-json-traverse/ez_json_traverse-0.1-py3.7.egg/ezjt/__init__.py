"""Easier JSON navigation and exploration."""

from typing import Any, Mapping, Sequence, Optional, Union, Dict, List
from pprint import pformat


__all__ = ('EZJL', 'EZJD', 'as_traversable', 'traverse')


EZJsonValues = Optional[Union['EZJL', 'EZJD', str, float, int]]

DEFAULT_SEP = '.'


def traverse(value, path, sep: str = DEFAULT_SEP):
    # Non-string path
    if isinstance(path, (int, slice)):
        return value[path]
    if not isinstance(path, str):
        error_msg = f'Unsupported path {path!r} of type {type(path).__name__}'
        if isinstance(value, list):
            raise IndexError(error_msg)
        raise KeyError(error_msg)

    traversed = []
    parent = as_traversable(value, parent = None, sep = sep)
    remaining = path.split(sep)
    while remaining:
        bit = remaining.pop(0)
        error_msg = f'Error traversing {path!r}, failed from {sep.join(traversed)!r} to {bit!r}: '  # noqa
        try:
            parent = as_traversable(value, parent = parent, sep = sep)
        except ValueError as e:
            raise ValueError(error_msg + 'bad value') from e

        # Handle list
        if isinstance(value, list):
            map_ret = False
            try:
                if ':' in bit:
                    if bit.endswith('m'):
                        map_ret = True
                        bit = bit[:-1]
                    index = slice(*map(int, bit.split(':')))
                else:
                    index = int(bit)
            except (ValueError, TypeError):
                raise IndexError(error_msg + 'bad sequence index')
            try:
                value = value[index]
            except IndexError:
                raise IndexError(error_msg + 'index does not exist')
            if map_ret:
                retval = []
                for n, val in enumerate(value):
                    try:
                        retval.append(traverse(val, sep.join(remaining), sep))
                    except (KeyError, IndexError) as e:
                        raise IndexError(error_msg + f'failed on {n}') from e
                return as_traversable(retval, sep = sep)

        # Handle dict
        elif isinstance(value, dict):
            try:
                value = value[bit]
            except KeyError:
                raise KeyError(error_msg + 'no such key')
    if isinstance(value, (list, dict)):
        return as_traversable(value, parent = parent, sep = sep)
    return value


class _EZBase:

    def __init__(self, underlying, *,
                 parent: Optional[Union['EZJL', 'EZJD']] = None,
                 sep: str = DEFAULT_SEP):
        self._underlying = underlying
        self._parent = parent
        self._sep = sep

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def __iter__(self) -> Iterator[str]:
        return iter(self._underlying)

    def __getitem__(self, path) -> EZJsonValues:
        return traverse(self._underlying, path, self._sep)

    def __len__(self) -> int:
        return len(self._underlying)

    def __repr__(self) -> str:
        name = type(self).__name__
        sep = '\n' + ' ' * (len(name) + 1)
        blob = sep.join(pformat(self._underlying, compact=True).splitlines())
        return f'{name}({blob},{sep}{sep}sep={self._sep!r})'


class EZJL(_EZBase, Sequence[EZJsonValues]):
    pass


class EZJD(_EZBase, Mapping[str, EZJsonValues]):
    pass


def as_traversable(value: Union[Dict[str, Any], List[Any]], *,
                   parent: Optional[Union[EZJL, EZJD]] = None,
                   sep: str = DEFAULT_SEP):
    if isinstance(value, list):
        return EZJL(value, parent = parent, sep = sep)
    elif isinstance(value, dict):
        return EZJD(value, parent = parent, sep = sep)
    else:
        raise ValueError(f'Bad type, unexpected {type(value).__name__}')
