
from typing import NewType


# ------------------------------------------------------------------------------
# 'pylint --load_-plugins hotdog_checker hot_dog.py
# ------------------------------------------------------------------------------

class HotDog:
    pass

ReadyToServeHotDog = NewType("ReadyToServeHotDog", HotDog)

def create_hot_dog() -> ReadyToServeHotDog:
    hot_dog = HotDog()
    return ReadyToServeHotDog(hot_dog)

def create(): 
    hot_dog=ReadyToServeHotDog(HotDog())
