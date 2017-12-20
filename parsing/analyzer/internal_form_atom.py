

class InternalFormAtom:

    def __init__(self, key_code: int, category_code: int):
        self.__key_code = key_code
        self.__category_code = category_code

    @property
    def key(self):
        return self.__key_code

    @property
    def category(self):
        return self.__category_code

    def __str__(self):
        return '{}|{}'.format(self.__key_code, self.__category_code)

    def __repr__(self):
        return str(self)
