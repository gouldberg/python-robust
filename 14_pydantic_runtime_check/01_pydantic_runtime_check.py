
import pprint
import yaml
from typing import Literal, List, Optional, TypedDict, Union

from pydantic import conlist, constr, PositiveInt, ValidationError
from pydantic.dataclasses import dataclass
from pydantic import validator
from pydantic import StrictInt


# ----------
print_orig = print
print = pprint.pprint


fpath_restaurant = '14_pydantic_runtime_check/restaurant.yaml'
fpath_restaurant_missing = '14_pydantic_runtime_check/missing.yaml'
fpath_restaurant_wrongtype = '14_pydantic_runtime_check/wrong_type.yaml'


# ------------------------------------------------------------------------------
# pydantic is parser.
# pydantic try to convert string to integer (pydantic do best)
# ------------------------------------------------------------------------------

@dataclass
class Model:
    value: int


# pydantic is parser.
# pydantic try to convert string to integer (pydantic do best)
Model(value="123")


# pydantic check value:  ValidationError
Model(value=5.5)


# ----------
@dataclass
class Model2:
    value: StrictInt


# pydantic is parser,
# but of StrictInt is specified, ValidationError
Model2(value="0023")


# ------------------------------------------------------------------------------
# read restaurant.yaml
# ------------------------------------------------------------------------------

# load yaml file in dictionary
with open(fpath_restaurant) as yaml_file:
    restaurant = yaml.safe_load(yaml_file)


print(restaurant)


# ------------------------------------------------------------------------------
# in order to test,
# convert yaml (dictionary) nested data
# to class with TypedDict
# ------------------------------------------------------------------------------

class AccountAndRoutingNumber(TypedDict):
    account_number: str
    routing_number: str


class BankDetails(TypedDict):
    bank_details: AccountAndRoutingNumber


class Address(TypedDict):
    address: str


AddressOrBankDetails = Union[Address, BankDetails]


Position = Literal['Chef', 'Sous Chef', 'Host',
                   'Server', 'Delivery Driver']

class Dish(TypedDict):
    name: str
    price_in_cents: int
    description: str


class DishWithOptionalPicture(Dish, TypedDict, total=False):
    picture: str


class Employee(TypedDict):
    name: str
    position: Position
    payment_details: AddressOrBankDetails


class Restaurant(TypedDict):
    name: str
    owner: str
    address: str
    employees: list[Employee]
    dishes: list[Dish]
    number_of_seats: int
    to_go: bool
    delivery: bool


# -----------
# Now the type hint is class Restaurant
def load_restaurant(filename: str) -> Restaurant:
    with open(filename) as yaml_file:
        return yaml.safe_load(yaml_file)


load_restaurant(fpath_restaurant)


# -->
# but methods can not be added to TypeDict.
# TypeDict does not have validation check (implicitly)


# ------------------------------------------------------------------------------
# Not inherit TypeDict
# but decorate by pydantic.dataclasses.dataclass
# ------------------------------------------------------------------------------

@dataclass
class AccountAndRoutingNumber():
    account_number: str
    routing_number: str


@dataclass
class BankDetails:
    bank_details: AccountAndRoutingNumber


@dataclass
class Address:
    address: str


AddressOrBankDetails = Union[Address, BankDetails]


Position = Literal['Chef', 'Sous Chef', 'Host',
                   'Server', 'Delivery Driver']


@dataclass
class Dish:
    name: str
    price_in_cents: int
    description: str
    picture: Optional[str] = None


@dataclass
class Employee:
    name: str
    position: Position
    payment_details: AddressOrBankDetails


@dataclass
class Restaurant:
    name: str
    owner: str
    address: str
    employees: list[Employee]
    dishes: list[Dish]
    number_of_seats: int
    to_go: bool
    delivery: bool


def load_restaurant(filename: str) -> Restaurant:
    with open(filename) as yaml_file:
        data = yaml.safe_load(yaml_file)
        return Restaurant(**data)


restaurant = load_restaurant(fpath_restaurant)


# dish of Caprese Salad does not have description.
restaurant = load_restaurant(fpath_restaurant_missing)


# ------------------------------------------------------------------------------
# use builtin vali data. (custom data type to check particular constrain of the field)
# ------------------------------------------------------------------------------

# limit string length
@dataclass
class AccountAndRoutingNumber:
    account_number: constr(min_length=9, max_length=9)
    routing_number: constr(min_length=8, max_length=12)


@dataclass
class BankDetails:
    bank_details: AccountAndRoutingNumber


# limit string length
@dataclass
class Address:
    address: constr(min_length=1)


AddressOrBankDetails = Union[Address, BankDetails]


Position = Literal['Chef', 'Sous Chef', 'Host',
                   'Server', 'Delivery Driver']

@dataclass
class Employee:
    name: str
    position: Position
    payment_details: AddressOrBankDetails


# limit string length
@dataclass
class Dish:
    name: constr(min_length=1, max_length=16)
    price_in_cents: PositiveInt
    description: constr(min_length=1, max_length=80)
    picture: Optional[str] = None


# limit string length
# only string matched by the specified expression is allowed.
@dataclass
class Restaurant:
    name: constr(regex=r'^[a-zA-Z0-9 ]*$',
                  min_length=1, max_length=16)
    owner: constr(min_length=1)
    address: constr(min_length=1)
    employees: list[Employee]
    dishes: list[Dish]
    number_of_seats: PositiveInt
    to_go: bool
    delivery: bool


restaurant = Restaurant(**{
    'name': 'Dine-n-Dash',
    'owner': 'Pat Viafore',
    'address': '123 Fake St.',
    'employees': [],
    'dishes': [],
    'number_of_seats': -5,
    'to_go': False,
    'delivery': True
})


# ----------
# employees is limited list of Employee class and minimum 2
# dishes is limited list of Dish class and minimum 3
@dataclass
class Restaurant:
    name: constr(min_length=1, max_length=16)
    owner: constr(min_length=1)
    address: constr(min_length=1)
    employees: conlist(Employee, min_items=2)
    dishes: conlist(Dish, min_items=3)
    number_of_seats: PositiveInt
    to_go: bool
    delivery: bool


restaurant = load_restaurant(fpath_restaurant_missing)


# ------------------------------------------------------------------------------
# @validator 
# ------------------------------------------------------------------------------

@dataclass
class AccountAndRoutingNumber:
    account_number: constr(min_length=9,max_length=9)
    routing_number: constr(min_length=8,max_length=12)


@dataclass
class BankDetails:
    bank_details: AccountAndRoutingNumber


@dataclass
class Address:
    address: constr(min_length=1)


AddressOrBankDetails = Union[Address, BankDetails]


Position = Literal['Chef', 'Sous Chef', 'Host',
                   'Server', 'Delivery Driver']


@dataclass
class Employee:
    name: str
    position: Position


@dataclass
class Dish:
    name: constr(min_length=1, max_length=16)
    price_in_cents: PositiveInt
    description: constr(min_length=1, max_length=80)
    picture: Optional[str] = None


@dataclass
class Restaurant:
    name: constr(regex=r'^[a-zA-Z0-9 ]*$',
                   min_length=1, max_length=16)
    owner: constr(min_length=1)
    address: constr(min_length=1)
    employees: conlist(Employee, min_items=2)
    dishes: conlist(Dish, min_items=3)
    number_of_seats: PositiveInt
    to_go: bool
    delivery: bool

    @validator('employees')
    def check_chef_and_server(cls, employees):
        if (any(e for e in employees if e.position == 'Chef') and 
            any(e for e in employees if e.position == 'Server')):
                return employees
        raise ValueError('Must have at least one chef and one server')


restaurant = Restaurant(**{
    'name': 'Dine n Dash',
    'owner': 'Pat Viafore',
    'address': '123 Fake St.',
    'employees': [Employee('Pat', 'Chef'), Employee('Joe', 'Chef')],
    'dishes': [Dish('abc'), Dish('def'), Dish('ghi')],
    'number_of_seats': 5,
    'to_go': False,
    'delivery': True
})

restaurant = load_restaurant(fpath_restaurant_missing)
