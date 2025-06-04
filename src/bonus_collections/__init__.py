from __future__ import annotations

from collections.abc import Iterator, Sequence
from copy import deepcopy
from itertools import islice
from operator import index
from typing import Generic, Self, SupportsIndex, TypeVar, overload

T_co = TypeVar("T_co", covariant=True)


class Subsequence(Generic[T_co], Sequence[T_co]):
    """A view of a section of a sequence

    Behaves similarly to seq[start:stop:step] but is a view rather than a copy.
    """

    __slots__ = ("_source", "_range")

    _source: Sequence[T_co]
    _range: slice[int, int, int]

    def __init__(self, seq: Sequence[T_co], section: slice[int, int, int]) -> None:
        section = slice(*section.indices(len(seq)))
        if isinstance(seq, Subsequence):
            self._source = seq._source
            step: int = seq._range.step * section.step
            self._range = slice(
                seq._range.start + section.start * seq._range.step,
                (max if step < 0 else min)(
                    seq._range.stop, seq._range.start + section.stop * seq._range.step
                ),
                step,
            )
        else:
            self._source = seq
            self._range = section

    def __bool__(self) -> bool:
        return self._range.stop != self._range.start and (
            self._range.stop > self._range.start
        ) == (self._range.step >= 0)

    def __copy__(self) -> Self:
        return self

    def __deepcopy__(self) -> Self:
        return type(self)([deepcopy(element) for element in self], slice(None))

    @overload
    def __getitem__(self, i: SupportsIndex, /) -> T_co:
        pass

    @overload
    def __getitem__(
        self, s: slice[SupportsIndex, SupportsIndex, SupportsIndex], /
    ) -> Self:
        pass

    def __getitem__(
        self, key: SupportsIndex | slice[SupportsIndex, SupportsIndex, SupportsIndex], /
    ) -> T_co | Self:
        if isinstance(key, slice):
            return type(self)(
                self._source, slice(index(key.start), index(key.stop), index(key.step))
            )
        else:
            i: int = index(key)
            return self._source[self._range.start + self._range.step * i]

    def __len__(self) -> int:
        return (self._range.stop - self._range.start) // self._range.step

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._source!r}, {self._range!r})"

    def __str__(self) -> str:
        start_str: str = "" if self._range.start is None else str(self._range.start)
        stop_str: str = "" if self._range.stop is None else str(self._range.stop)
        step_str: str = "" if self._range.step is None else f":{self._range.step}"
        return f"{self._source}[{start_str}:{stop_str}{step_str}]"


__all__ = ["Subsequence"]
