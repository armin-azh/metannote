from typing import Dict, List, Tuple, Union
import numpy as np

NDARRAY = np.ndarray
ANNOTATIONS = Dict[int, List[dict]]
COCO = Tuple[List[dict], dict]
BOX = Union[List[int], Tuple[int], NDARRAY]
