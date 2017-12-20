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

    @property
    def atom_keys(self) -> List[str]:
        groups = zip(*[list(map(lambda x: x.key, self.__atoms))[index::2] for index in range(2)])
        other = [('12', 'ε', '13') if x == ('12', '13') else x for x in groups]
        return [key for group in list(map(lambda x: list(x), other)) for key in group]
