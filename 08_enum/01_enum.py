
from enum import auto, Enum, Flag, IntEnum, unique
from typing import Set, List, Literal


# ------------------------------------------------------------------------------
# tuple
# ------------------------------------------------------------------------------

MOTHER_SAUCES = (
    "Béchamel",
    "Velouté",
    "Espagnole",
    "Tomato",
    "Hollandaise",
)


# access by integer index
MOTHER_SAUCES[2]


# ------------------------------------------------------------------------------
# use tuple as passed argument
# ------------------------------------------------------------------------------

BÉCHAMEL = "Béchamel"
VELOUTÉ = "Velouté"
ESPAGNOLE = "Espagnole"
TOMATO = "Tomato"
HOLLANDAISE = "Hollandaise"

def create_daughter_sauce(mother_sauce: str, extra_ingredients: list[str]):
    pass


# ----------
create_daughter_sauce(MOTHER_SAUCES[0], ["Béchamel"])

create_daughter_sauce(BÉCHAMEL, ["Béchamel"])


# ------------------------------------------------------------------------------
# Enum
#   - does not allow accessing to non-exist attribute/member
#   - function signature is clearer
# ------------------------------------------------------------------------------

class MotherSauce(Enum):
    BÉCHAMEL = "Béchamel"
    VELOUTÉ = "Velouté"
    ESPAGNOLE = "Espagnole"
    TOMATO = "Tomato"
    HOLLANDAISE = "Hollandaise"


# ----------
# access by attribute/member, 'name' and 'value'
MotherSauce.BÉCHAMEL
MotherSauce.BÉCHAMEL.name
MotherSauce.BÉCHAMEL.value

MotherSauce.HOLLANDAISE
MotherSauce.HOLLANDAISE.name
MotherSauce.HOLLANDAISE.value


# ----------
# access by value: OK
MotherSauce("Hollandaise")

# if accessed to non-existed value
# ValueError
try:
    MotherSauce("Alabama White BBQ Sauce")
    assert False, "Should not consider BBQ sauce a mother sauce"
except:
    pass


# ----------
# iterate
print(list(enumerate(MotherSauce, start=1)))

assert list(enumerate(MotherSauce, start=1)) == [(1, MotherSauce.BÉCHAMEL), (2, MotherSauce.VELOUTÉ), (3, MotherSauce.ESPAGNOLE),
                                                 (4, MotherSauce.TOMATO), (5,MotherSauce.HOLLANDAISE)]


# ----------
# function signature is clearer than tuple case.
def create_daughter_sauce(mother_sauce: MotherSauce, 
                          extra_ingredients: list[str]):
    pass 

create_daughter_sauce(MotherSauce.TOMATO, [])


# ------------------------------------------------------------------------------
# auto()
# ------------------------------------------------------------------------------

class MotherSauce(Enum):
    BÉCHAMEL = auto()
    VELOUTÉ = auto()
    ESPAGNOLE = auto()
    TOMATO = auto()
    HOLLANDAISE = auto()


# ----------
# access by attribute/member name
# auto() assigns integer increasing by 1 starting from 0 automatically.
MotherSauce.BÉCHAMEL
MotherSauce.BÉCHAMEL.name
MotherSauce.BÉCHAMEL.value

MotherSauce.HOLLANDAISE
MotherSauce.HOLLANDAISE.name
MotherSauce.HOLLANDAISE.value


# ----------
list(MotherSauce)

assert repr(list(MotherSauce)) =="[<MotherSauce.BÉCHAMEL: 1>, <MotherSauce.VELOUTÉ: 2>, <MotherSauce.ESPAGNOLE: 3>, <MotherSauce.TOMATO: 4>, <MotherSauce.HOLLANDAISE: 5>]"


# ------------------------------------------------------------------------------
# auto():  if you would like to specify values
# override _generate_next_value_()
# ------------------------------------------------------------------------------

class MotherSauce(Enum):

    # override:  now convert ABC --> Abc (capitalize)
    def _generate_next_value_(name: str, start, count, last_values): # type: ignore
        return name.capitalize()

    # but still use auto()
    BÉCHAMEL = auto()
    VELOUTÉ = auto()
    ESPAGNOLE = auto()
    TOMATO = auto()
    HOLLANDAISE = auto()


MotherSauce.BÉCHAMEL
MotherSauce.BÉCHAMEL.name

# now value is not 1, but capitalized name
MotherSauce.BÉCHAMEL.value

assert repr(list(MotherSauce)) =="[<MotherSauce.BÉCHAMEL: 'Béchamel'>, <MotherSauce.VELOUTÉ: 'Velouté'>, <MotherSauce.ESPAGNOLE: 'Espagnole'>, <MotherSauce.TOMATO: 'Tomato'>, <MotherSauce.HOLLANDAISE: 'Hollandaise'>]"


# ----------
class PowersOfThree(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return 3 ** (count + 1)
    FIRST = auto()
    SECOND = auto()


PowersOfThree.FIRST.value

PowersOfThree.SECOND.value


# ------------------------------------------------------------------------------
# Enum --> Flag 
# ------------------------------------------------------------------------------

class Allergen(Enum):
    FISH = auto()
    SHELLFISH = auto()
    TREE_NUTS = auto()
    PEANUTS = auto()
    GLUTEN = auto()
    SOY = auto()
    DAIRY = auto()
    

# allergens collection is created by set
allergens: set[Allergen] = {Allergen.FISH, Allergen.SOY}

allergens


# -----------
# Enum --> Flag
# Flags _generate_next_value_() create not integer increasing by 1 but integer of power of 2

class Allergen(Flag):
    FISH = auto()
    SHELLFISH = auto()
    TREE_NUTS = auto()
    PEANUTS = auto()
    GLUTEN = auto()
    SOY = auto()
    DAIRY = auto()
    SEAFOOD = FISH | SHELLFISH
    ALL_NUTS = TREE_NUTS | PEANUTS


Allergen.SEAFOOD
Allergen.SEAFOOD.name

# ----------
# this values is 3 (FISH 0, SHELLFISH 1)
Allergen.SEAFOOD.value

# allergens collection is created now not by set, but by flags
allergens = Allergen.FISH | Allergen.SHELLFISH

assert repr(allergens) == "<Allergen.SEAFOOD: 3>"

assert allergens & Allergen.FISH


# ------------------------------------------------------------------------------
# Enum --> IntEnum
# Flag --> IntFlag
#   allows comparison with integer value
# ------------------------------------------------------------------------------

class ImperialLiquidMeasure(Enum):
    CUP = 8
    PINT = 16
    QUART = 32
    GALLON = 128


# Enum does not allow comparison with integer value
assert ImperialLiquidMeasure.CUP == 8
assert ImperialLiquidMeasure.CUP != 8

# this is OK
assert ImperialLiquidMeasure.CUP.value == 8


# ----------
class ImperialLiquidMeasure(IntEnum):
    CUP = 8
    PINT = 16
    QUART = 32
    GALLON = 128

# IntEnum allows comparison with integer value
assert ImperialLiquidMeasure.CUP == 8
assert ImperialLiquidMeasure.CUP.value == 8


# ----------
# but if comparison with integer value is possible,
# small change will be bugs

# now someone update this value itself or add more member, following code will be bugs ...
# BETTER TO USE auto() here.
class Kitchenware(IntEnum):
    # Note to future programmers: these numbers are customer-defined 
     # and apt to change
     PLATE = 7
     CUP = 8
     UTENSILS = 9

def pour_into_larger_vessel():
    pass

def pour_into_smaller_vessel():
    pass

def pour_liquid(volume: ImperialLiquidMeasure):
    if volume == Kitchenware.CUP:
        pour_into_smaller_vessel()
    else:
        pour_into_larger_vessel()

pour_liquid(ImperialLiquidMeasure.CUP)


# ------------------------------------------------------------------------------
# @unique:  does not allow duplicated keys
# ------------------------------------------------------------------------------

# key is not duplicated, but value is duplicated
class MotherSauce(Enum):
    BÉCHAMEL = "Béchamel"
    BECHAMEL = "Béchamel"
    VELOUTÉ = "Velouté"
    VELOUTE = "Velouté"
    ESPAGNOLE = "Espagnole"
    TOMATO = "Tomato"
    HOLLANDAISE = "Hollandaise"

MotherSauce.BÉCHAMEL
MotherSauce.BÉCHAMEL


# ----------
# This does not allow duplicated keys by @unique

@unique
class MotherSauce(Enum):
    BÉCHAMEL = "Béchamel"
    VELOUTÉ = "Velouté"
    ESPAGNOLE = "Espagnole"
    TOMATO = "Tomato"
    HOLLANDAISE = "Hollandaise"


# ValueError: duplicate values found in ...
@unique
class MotherSauce(Enum):
    BÉCHAMEL = "Béchamel"
    BECHAMEL = "Béchamel"
    VELOUTÉ = "Velouté"
    VELOUTE = "Velouté"
    ESPAGNOLE = "Espagnole"
    TOMATO = "Tomato"
    HOLLANDAISE = "Hollandaise"
