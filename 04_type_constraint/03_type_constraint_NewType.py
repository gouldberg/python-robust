
from typing import NewType
from dataclasses import dataclass


# NewType:


# ------------------------------------------------------------------------------
# NewType
#   can make new data type. 
# ------------------------------------------------------------------------------

class HotDog:
    pass
    

# ----------
# dispense_to_customer take new type ReadyToServeHotDog
ReadyToServeHotDog = NewType("ReadyToServeHotDog", HotDog)

def dispense_to_customer(hot_dog: ReadyToServeHotDog):
    pass


# ----------
# If you run 'mypy <this script>' produce:
#   Argument 1 to "dispense_to_customer" has incompatible type "HotDog"; expected "ReadyToServeHotDog" [arg-type]
dispense_to_customer(HotDog())

# type check successful
dispense_to_customer(ReadyToServeHotDog(HotDog()))



# ------------------------------------------------------------------------------
# create new type by returning converted original class
# convert to not-ready-to-serve HotDog to ReadyToServeHotDog
# ------------------------------------------------------------------------------

class HotDog:
    pass
    

ReadyToServeHotDog = NewType("ReadyToServeHotDog", HotDog)


# ----------
# return ReadyToServeHotDog
def prepare_for_serving(hot_dog: HotDog) -> ReadyToServeHotDog:
    assert not hot_dog.is_plated(), "hot dog in not on plate"
    hot_dog.put_on_plate()
    hot_dog.add_napkins()
    return ReadyToServeHotDog(hot_dog)
