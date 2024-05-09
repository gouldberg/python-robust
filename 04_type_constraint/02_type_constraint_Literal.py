
from typing import Literal
from dataclasses import dataclass


# Literals:
# Literal types let you indicate that an expression is equal to some specific primitive value.


# ------------------------------------------------------------------------------
# Parameterizing Literals
# Literals may also contain aliases to other literal types
# ------------------------------------------------------------------------------

PrimaryColors = Literal["red", "blue", "yellow"]

SecondaryColors = Literal["purple", "green", "orange"]

AllowedColors = Literal[PrimaryColors, SecondaryColors]


def paint(color: AllowedColors) -> None:
    pass

paint("red")        # Type checks!

paint("turquoise")  # Does not type check



# ------------------------------------------------------------------------------
# Literal example
# ------------------------------------------------------------------------------

@dataclass
class Error:
    error_code: Literal[1,2,3,4,5]
    disposed_of: bool


@dataclass
class Snack:
    name: Literal["Pretzel", "Hot Dog"]
    condiments: set[Literal["Mustard", "Ketchup"]]


# to be error ...
Error(0, False)

Snack("Not Valid", set())

Snack("Pretzel", {"Mustard", "Relish"})

