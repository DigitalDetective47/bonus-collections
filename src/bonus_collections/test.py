from collections.abc import Sequence
from unittest import TestCase, main

from . import Subsequence


class TestSubsequence(TestCase):
    __slots__ = ("base_seq",)

    base_seq: Sequence[object]

    def setUp(self) -> None:
        self.base_seq = tuple(range(10))

    def test_basic(self) -> None:
        self.assertEqual(
            self.base_seq[3:8], tuple(Subsequence(self.base_seq, slice(3, 8)))
        )

    def test_getitem(self) -> None:
        self.assertEqual(
            self.base_seq[3:8][2], Subsequence(self.base_seq, slice(3, 8))[2]
        )

    def test_step(self) -> None:
        self.assertEqual(
            self.base_seq[3:8:2], tuple(Subsequence(self.base_seq, slice(3, 8, 2)))
        )

    def test_recursive(self) -> None:
        self.assertEqual(
            self.base_seq[3:8:2][:3],
            tuple(Subsequence(Subsequence(self.base_seq, slice(3, 8, 2)), slice(3))),
        )

    def test_negative(self) -> None:
        self.assertEqual(
            self.base_seq[3:-1], tuple(Subsequence(self.base_seq, slice(3, -1)))
        )


if __name__ == "__main__":
    main()
