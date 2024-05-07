
import datetime

from dataclasses import dataclass, FrozenInstanceError
from typing import Set
from enum import auto, Enum
from collections import namedtuple

from copy import deepcopy


# ------------------------------------------------------------------------------
# namedtuple is more readable compared to tuple
# ------------------------------------------------------------------------------

NutritionInformation = namedtuple('NutritionInformation', ['calories', 'fat', 'carbohydrates'])

nutrition = NutritionInformation(calories=100, fat=5, carbohydrates=10)

assert nutrition.calories == 100


# ------------------------------------------------------------------------------
# dataclass requires field type or default value
# ------------------------------------------------------------------------------

# dataclass requires field type or default value
@dataclass
class MyFraction:
    numerator: int = 0
    denominator: int = 1


# ----------
# dataclass is supporting __str__() amd __repr__()
frac = MyFraction()

str(frac)
repr(frac)
    

# ------------------------------------------------------------------------------
# dataclass:  nested
# ------------------------------------------------------------------------------

class ImperialMeasure(Enum): # <1>
    TEASPOON = auto()
    TABLESPOON = auto()
    CUP = auto()


class Broth(Enum): # <2>
    VEGETABLE = auto()
    CHICKEN = auto()
    BEEF = auto()
    FISH = auto()


# ----------
# now type of a member 'units' is ImperialMeasure and default value is CUP
# frozen=True means immutable

@dataclass(frozen=True) # <3>
class Ingredient:
    name: str
    amount: float = 1
    units: ImperialMeasure = ImperialMeasure.CUP


# ----------
# nested dataclass:  Ingredient is itself dataclass
@dataclass(frozen=True)
class Recipe:
    aromatics: set[Ingredient]
    broth: Broth
    vegetables: set[Ingredient]
    meats: set[Ingredient]
    starches: set[Ingredient]
    garnishes: set[Ingredient]
    time_to_cook: datetime.timedelta


# ----------
# generate Ingredient instances
pepper = Ingredient("Pepper", 1, ImperialMeasure.TABLESPOON)
garlic = Ingredient("Garlic", 2, ImperialMeasure.TEASPOON)
carrots = Ingredient("Carrots", .25, ImperialMeasure.CUP)
celery = Ingredient("Celery", .25, ImperialMeasure.CUP)
onions = Ingredient("Onions", .25, ImperialMeasure.CUP)
parsley = Ingredient("Parsley", 2, ImperialMeasure.TABLESPOON)
noodles = Ingredient("Noodles", 1.5, ImperialMeasure.CUP)
chicken = Ingredient("Chicken", 1.5, ImperialMeasure.CUP)

# generate Recipe instance, using Ingredient instances
soup = Recipe(
    aromatics={pepper, garlic},
    broth=Broth.CHICKEN,
    vegetables={celery, onions, carrots},
    meats={chicken},
    starches={noodles},
    garnishes={parsley},
    time_to_cook=datetime.timedelta(minutes=60))


# ----------
# dataclass is supporting __str__() amd __repr__()
str(soup)
repr(soup)


# ------------------------------------------------------------------------------
# dataclass:  frozen=True to make immutable the class itself, but still member itself is mutable
# ------------------------------------------------------------------------------

soup.broth


# Recipe is immutable and try to assign new value to soup.broth
try:
    # this is an error
    soup.broth = Broth.VEGETABLE # type: ignore
    assert False
except FrozenInstanceError as e:
    pass 


# ----------
# this is not an error
# Recipe is immutable,
# but if its attribute itself is mutable, you can modify it.
soup = Recipe(
    aromatics=set(),
    broth=Broth.CHICKEN,
    vegetables=set(),
    meats=set(),
    starches=set(),
    garnishes=set(), 
    time_to_cook=datetime.timedelta(seconds=3600))

# can add
soup.aromatics.add(Ingredient("Garlic"))


# ------------------------------------------------------------------------------
# dataclass implemented with methods
# ------------------------------------------------------------------------------

class ImperialMeasure(Enum): # <1>
    TEASPOON = auto()
    TABLESPOON = auto()
    CUP = auto()


class Broth(Enum): # <2>
    VEGETABLE = auto()
    CHICKEN = auto()
    BEEF = auto()
    FISH = auto()


@dataclass(frozen=True) # <3>
class Ingredient:
    name: str
    amount: float = 1
    units: ImperialMeasure = ImperialMeasure.CUP


# now Recipe dataclass is implemented with methods
# eq=True:  support ==, != operator.
@dataclass(eq=True)
class Recipe: # <4>
    aromatics: set[Ingredient]
    broth: Broth
    vegetables: set[Ingredient]
    meats: set[Ingredient]
    starches: set[Ingredient]
    garnishes: set[Ingredient]
    time_to_cook: datetime.timedelta

    def make_vegetarian(self):
        self.meats.clear()
        self.broth = Broth.VEGETABLE

    def get_ingredient_names(self):
        ingredients = (self.aromatics | 
                       self.vegetables |
                       self.meats |
                       self.starches |
                       self.garnishes)              

        return ({i.name for i in ingredients} |
                {self.broth.name.capitalize() + " Broth"})


# ----------
# generate Ingredient instances and Recipe instance

pepper = Ingredient("Pepper", 1, ImperialMeasure.TABLESPOON)
garlic = Ingredient("Garlic", 2, ImperialMeasure.TEASPOON)
carrots = Ingredient("Carrots", .25, ImperialMeasure.CUP)
celery = Ingredient("Celery", .25, ImperialMeasure.CUP)
onions = Ingredient("Onions", .25, ImperialMeasure.CUP)
parsley = Ingredient("Parsley", 2, ImperialMeasure.TABLESPOON)
noodles = Ingredient("Noodles", 1.5, ImperialMeasure.CUP)
chicken = Ingredient("Chicken", 1.5, ImperialMeasure.CUP)

chicken_noodle_soup = Recipe(
    aromatics={pepper, garlic},
    broth=Broth.CHICKEN,
    vegetables={celery, onions, carrots},
    meats={chicken},
    starches={noodles},
    garnishes={parsley},
    time_to_cook=datetime.timedelta(minutes=60))


# ----------
assert chicken_noodle_soup.broth == Broth.CHICKEN

chicken_noodle_soup.garnishes.add(pepper)

assert chicken_noodle_soup.garnishes == {parsley, pepper}


# ----------
# deepcopy in order to avoid modifying chicken_noodle_soup instance
noodle_soup = deepcopy(chicken_noodle_soup)

# call method  (clear meats, etc.)
noodle_soup.make_vegetarian()

assert noodle_soup.get_ingredient_names() == {'Garlic', 'Pepper', 'Carrots', 'Celery', 'Onions', 'Noodles', 'Parsley', 'Vegetable Broth'}


# ----------
# eq=True:  supporting ==, != operator
assert noodle_soup == noodle_soup

assert chicken_noodle_soup != noodle_soup


# ------------------------------------------------------------------------------
# dataclass as default,
# does not support comparison (<. >, <=, >=) and can not be sorted
# ------------------------------------------------------------------------------

@dataclass(eq=True)
class NutritionInformation: #type: ignore
    calories: int
    fat: int
    carbohydrates: int

nutritionals = [NutritionInformation(calories=100, fat=1, carbohydrates=3),
                NutritionInformation(calories=50, fat=6, carbohydrates=4),
                NutritionInformation(calories=125, fat=12, carbohydrates=3)]


# dataclass as default,
# does not support comparison (<. >, <=, >=) and can not be sorted
try:
    sorted(nutritionals) # type: ignore
    assert False
except TypeError as e:
    pass


# ------------------------------------------------------------------------------
# eq=True and order=True to support sorting
# ------------------------------------------------------------------------------

@dataclass(eq=True, order=True)
class NutritionInformation: # type: ignore
    calories: int
    fat: int
    carbohydrates: int

nutritionals = [NutritionInformation(calories=100, fat=1, carbohydrates=3),
                NutritionInformation(calories=50, fat=6, carbohydrates=4),
                NutritionInformation(calories=125, fat=12, carbohydrates=3)]

assert sorted(nutritionals) == [NutritionInformation(calories=50, fat=6, carbohydrates=4), # type: ignore
                                NutritionInformation(calories=100, fat=1, carbohydrates=3),
                                NutritionInformation(calories=125, fat=12, carbohydrates=3)] 


# ------------------------------------------------------------------------------
# Override special methods to change definition/order of comparison
# ------------------------------------------------------------------------------

# now NOT specify order=True 

@dataclass(eq=True)
class NutritionInformation: # type: ignore
    calories: int
    fat: int
    carbohydrates: int

    # now change comparison order:  firstly 'fat', secondly 'carbohydrates' and the third 'calories'
    def __lt__(self, rhs) -> bool:
        return ((self.fat, self.carbohydrates, self.calories) < 
                (rhs.fat, rhs.carbohydrates, rhs.calories))

    def __le__(self, rhs) -> bool:
        return self < rhs or self == rhs

    def __gt__(self, rhs) -> bool:
        return not self <= rhs

    def __ge__(self, rhs) -> bool:
        return not self < rhs

nutritionals = [NutritionInformation(calories=100, fat=1, carbohydrates=3),
                NutritionInformation(calories=50, fat=6, carbohydrates=4),
                NutritionInformation(calories=125, fat=12, carbohydrates=3)]

assert sorted(nutritionals) ==[NutritionInformation(calories=100, fat=1, carbohydrates=3), NutritionInformation(calories=50, fat=6, carbohydrates=4), NutritionInformation(calories=125, fat=12, carbohydrates=3)] # type: ignore
