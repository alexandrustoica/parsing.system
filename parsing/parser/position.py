from typing import List

from parsing.domain.symbol import Symbol


class ParserPosition:

    def __init__(self, visited: List[Symbol], left: List[Symbol]):
        self._visited = visited
        self._left = left

    @property
    def visited(self) -> List[Symbol]:
        return self._visited

    @property
    def left(self) -> List[Symbol]:
        return self._left

    def go_next(self):
        return ParserPosition(self._visited + [self._left[0]], self._left[1:])

    def is_final(self) -> bool:
        return self._left == []

    def __str__(self):
        return "{}.{}".format("".join(map(lambda x: str(x), self.visited)),
                              "".join(map(lambda x: str(x), self.left)))
