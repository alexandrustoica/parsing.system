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
