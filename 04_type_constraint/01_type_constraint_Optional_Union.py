
from typing import Optional, Union, Set, Literal, Annotated
from dataclasses import dataclass


# ------------------------------------------------------------------------------
# automatic hot-dog stand
# ------------------------------------------------------------------------------

def dispense_bun():
    return Bun()

class HotDog:
    
    def add_condiments(self, *args):
        pass

class Bun:
    def add_frank(self, frank: str) -> HotDog:
        return HotDog()

def dispense_ketchup():
    return None

def dispense_mustard():
    return None

def dispense_frank() -> str:
    return "frank"

def dispense_hot_dog_to_customer(hot_dog: HotDog):
    pass

def create_hot_dog():
    bun = dispense_bun()
    frank = dispense_frank()
    hot_dog = bun.add_frank(frank)
    ketchup = dispense_ketchup()
    mustard = dispense_mustard()
    hot_dog.add_condiments(ketchup, mustard)
    dispense_hot_dog_to_customer(hot_dog)


# ----------
create_hot_dog()


# ------------------------------------------------------------------------------
# automatic hot-dog stand:
# defensive coding for AttributeError (None)
# ------------------------------------------------------------------------------

def dispense_bun():
    return Bun()

class HotDog:
    
    def add_condiments(self, *args):
        pass

class Bun:
    def add_frank(self, frank: str) -> HotDog:
        return HotDog()

def dispense_ketchup():
    return None

def dispense_mustard():
    return None

def dispense_frank() -> str:
    return "frank"

def dispense_hot_dog_to_customer(hot_dog: HotDog):
    pass

# defensive coding for AttributeError (None)
def create_hot_dog():
    bun = dispense_bun()
    if bun is None:
        print_error_code("Bun unavailable. Check for bun")
        return 

    frank = dispense_frank()
    if frank is None:
        print_error_code("Frank was not properly dispensed")
        return

    hot_dog = bun.add_frank(frank)
    if hot_dog is None:
        print_error_code("Hot Dog unavailable. Check for Hot Dog")
        return 

    ketchup = dispense_ketchup()
    mustard = dispense_mustard()
    if ketchup is None or mustard is None:
        print_error_code("Check for invalid catsup")
        return 

    hot_dog.add_condiments(ketchup, mustard)
    dispense_hot_dog_to_customer(hot_dog)


# ------------------------------------------------------------------------------
# Optional type
# ------------------------------------------------------------------------------

# Optional is optional among value exist or no value (here None)
maybe_a_string: Optional[str] = "abcdef"

maybe_a_string: Optional[str] = None



# ------------------------------------------------------------------------------
# type checker at default does not allow returning None
#   mypy <this script> produces error: 'Incompatible return value type (got "None", expected "Bun") [return-value]
# ------------------------------------------------------------------------------

class Bun:
    def __init__(self, args):
        pass


def are_buns_available():
    return False

# here return Bun not Optional[Bun]
def dispense_bun() -> Bun:
    # here return None and error by type checker at default.
    if not are_buns_available():
        return None
    return Bun('Wheat')


# def dispense_bun() -> Optional[Bun]:
#     if not are_buns_available():
#         return None
#     return Bun('Wheat')


assert dispense_bun() is None


# ------------------------------------------------------------------------------
# Union[int, str]:  variable can be used as int or str
#   Optional[int] is same as Union[int, None]
# ------------------------------------------------------------------------------

class HotDog:
    pass


class Pretzel:
    pass


def dispense_hot_dog() -> HotDog:
    return HotDog()


def dispense_pretzel() -> Pretzel:
    return Pretzel()


def dispense_snack(user_input: str) -> Union[HotDog, Pretzel]:
    if user_input == "Hot Dog":
        return dispense_hot_dog()
    elif user_input == "Pretzel":
        return dispense_pretzel()
    raise RuntimeError("Should never reach this code, as an invalid input has been")


# ------------------------------------------------------------------------------
# type product --> type sum:
# use Union to take into considerations invalid state
# to reduce value varieties (type product --> type sum)
# ------------------------------------------------------------------------------

# ----------
# dataclass case for Snack

# varieties of type product:
# 144 varieties (supposing, = name 3 * condiments 4 * error_code * 6 * disposed_of * 2)
@dataclass
class Snack:
    name: str
    condiments: set[str]
    error_code: int
    disposed_of: bool

Snack("Hotdog", {"Mustard", "Ketchup"}, 5, False)


# ----------
# use Union to take into considerations invalid state

# 10 varieties = error_code 5 (not including success 0) * disposed_of * 2
@dataclass
class Error:
    error_code: int
    disposed_of: bool


# 12 varieties = name 3 * condiments 4
@dataclass
class Snack:
    name: str
    condiments: set[str]


# snack will be Snack or Error:  10 + 12 = only 22 varieties
snack: Union[Snack, Error] = ("Hotdog", {"Mustard", "Ketchup"})

snack = Error(5, True)
