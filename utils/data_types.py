from enum import Enum
from typing import NewType

Model = NewType("Model", str)
class ModelTypes(Enum):
    STUFF = Model("stuff")
    MAP_REDUCE = Model("map_reduce")
    REFINE = Model("refine")
    MAP_RERANK = Model("map_rerank")


Dataset = NewType("Dataset", int)
class Datasets(Enum):
    ALL = Dataset(0)
    FRESHMAN = Dataset(1)
    SOPHOMORE = Dataset(2)
    JUNIOR = Dataset(3)
    SENIOR = Dataset(4)
