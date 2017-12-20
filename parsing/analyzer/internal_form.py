from typing import List
from parsing.analyzer.internal_form_atom import InternalFormAtom


class InternalForm:

    def __init__(self, file: str):
        with open(file) as data:
            self.__atoms = [InternalFormAtom(key.replace(' ', ''), category.replace(' ', ''))
                            for key, category in (line.split('|') for line in data.read().splitlines())]

    @property
    def atoms(self) -> List[InternalFormAtom]:
        return self.__atoms
