from enum import Enum


class ProductType(str, Enum):
    bottle = "bottle"
    can = "can"
    other = "other"


class ReturnLocation(str, Enum):
    billa = "Billa"
    spar = "Spar"
    hofer = "Hofer"
    lidl = "Lidl"
    penny = "Penny"