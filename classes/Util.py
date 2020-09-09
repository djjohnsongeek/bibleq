class Util():

    @staticmethod
    def contains_upper(string: str) -> bool:

        if type(string) != str:
            raise TypeError

        for char in string:
            if char.isupper():
                return True

        return False

    @staticmethod
    def contains_lower(string: str) -> bool:

        for char in string:
            if char.islower():
                return True

        return False

    @staticmethod
    def contains_num(string: str) -> bool:

        if type(string) != str:
            raise TypeError

        for char in string:
            if char.isnumeric():
                return True

        return False
