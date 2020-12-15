from abc import abstractmethod, ABC

from rich.table import Table


class AbstractBase:
    # Static Abstract Methods
    @staticmethod
    @abstractmethod
    def key() -> str:
        pass

    @staticmethod
    @abstractmethod
    def is_valid(value: str):
        pass

    @classmethod
    @abstractmethod
    def from_decimal(cls, number: int) -> str:
        pass

    # Overridable Static methods
    @classmethod
    def parse(cls, value):
        # If we were handed a decimal, get the string
        if isinstance(value, int):
            value = cls.from_decimal(value)

        # Otherwise, assume we were handed something valid?
        if not cls.is_valid(value):
            raise Exception("Invalid value")

        # So, we can now create this value
        return cls(value)

    @staticmethod
    def can_be_inferred() -> bool:
        return False

    @staticmethod
    def prefixes() -> list:
        return []

    @classmethod
    def is_inferred(cls, value: str) -> bool:
        if not cls.has_prefixes():
            return False

        return value[0:2] in cls.prefixes()

    @classmethod
    def has_prefixes(cls):
        return len(cls.prefixes()) > 0

    # Abstract Instance Methods
    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def base(self) -> int:
        pass

    # @staticmethod
    # def teach() -> str:
    #     return "Sorry, no lesson for this Base"
    #
    # @staticmethod
    # def formula() -> str:
    #     return "Sorry, no forumula for this Base"

    # Overridable methods
    def as_decimal(self) -> int:
        return int(self.value, self.base())

    def show_in_table(self) -> bool:
        return True

    def display(self):
        value = self.value
        if self.has_prefixes():
            for prefix in self.prefixes():
                value = value.replace(prefix, '')

        return value

    # Constructor
    def __init__(self, value: str):
        self.value = value
        self.is_given = False


class InferredBase(AbstractBase, ABC):
    @staticmethod
    def can_be_inferred() -> bool:
        return True


class Binary(InferredBase):

    @classmethod
    def from_decimal(cls, number: int) -> str:
        return bin(number)

    @staticmethod
    def prefixes() -> list:
        return ['0b']

    @staticmethod
    def is_valid(value: str):
        return True  # todo: if all 1s and 0s, after optional prefix

    @staticmethod
    def key() -> str:
        return 'bin'

    def title(self):
        return "Binary (2)"

    def base(self) -> int:
        return 2


class BinaryIndexed(Binary):

    @staticmethod
    def key() -> str:
        return 'bin-i'

    def title(self):
        return "Binary (2) - Indexed"

    def show_in_table(self) -> bool:
        return False

    def display(self, console=None):
        stripped = super().display()
        starting_index = int((2 ** len(stripped)) / 2)

        table = Table()

        # todo: a more pythonic way
        while starting_index >= 1:
            table.add_column(str(int(starting_index)))
            starting_index = starting_index / 2

        # todo: a more pythonic way
        indexes = []
        for r in range(len(stripped)):
            indexes.append(str(r))
        indexes.reverse()

        table.add_row(*indexes)
        table.add_row(*stripped)

        # todo: better formatting
        console.print(table)


class Octal(AbstractBase):
    @classmethod
    def from_decimal(cls, number: int) -> str:
        return oct(number)

    @staticmethod
    def prefixes() -> list:
        return ['0o']

    @staticmethod
    def is_valid(value: str):
        return True  # todo: try / except

    @staticmethod
    def key() -> str:
        return 'oct'

    def title(self):
        return "Octal (8)"

    def base(self) -> int:
        return 8


class Decimal(AbstractBase):
    @classmethod
    def from_decimal(cls, number: int) -> str:
        return str(number)

    @staticmethod
    def prefixes() -> list:
        return ['0d']

    @staticmethod
    def is_valid(value: str):
        return value.isdigit()

    @staticmethod
    def key() -> str:
        return 'dec'

    def title(self):
        return "Decimal (10)"

    def base(self) -> int:
        return 10


class Hexadecimal(InferredBase):
    @classmethod
    def from_decimal(cls, number: int) -> str:
        return hex(number)

    @staticmethod
    def prefixes() -> list:
        return ['0x']

    @staticmethod
    def is_valid(value: str):
        return True  # todo: try / except

    @staticmethod
    def key() -> str:
        return 'hex'

    def title(self):
        return "Hexadecimal"

    def base(self) -> int:
        return 16


# class Arbitrary(AbstractBase):  # todo

bases = {
    Binary.key(): Binary,
    BinaryIndexed.key(): BinaryIndexed,
    Octal.key(): Octal,
    Decimal.key(): Decimal,
    Hexadecimal.key(): Hexadecimal,
    # Arbitrary.key(): Arbitrary,
}
