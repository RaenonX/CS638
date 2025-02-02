"""
Controller of the MMT GTFS shape data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from typing import List, Dict, Tuple

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import MMTShape

__all__ = ("MMTShapeDataController", "ShapeIdNotFoundError")


class ShapeIdNotFoundError(KeyError):
    """Raised if the given shape ID is not found in the loaded data."""

    def __init__(self, shape_id: int):
        super().__init__(f"Data of shape ID <{shape_id}> not found")


class MMTShapeDataController(CSVLoadableController):
    """
    MMT shape data controller.

    Data file that will use this controller:
    - mmt_gtfs/shapes.csv
    """

    def _init_dict_by_id(self, shape: MMTShape):
        sid = shape.shape_id

        if sid not in self._dict_by_id:
            self._dict_by_id[sid] = []

        self._dict_by_id[sid].append(shape)

    def __init__(self, shapes: List[MMTShape]):
        """
        Initializes the shape data controller.

        Data in ``shapes`` should be pre-processed as following, or the functions may misbehave.

            GROUP BY shape_id, shape_pt_sequence ASC

        :param shapes: list of shape data
        """
        super().__init__(shapes)

        self._dict_by_id: Dict[int, List[MMTShape]] = {}

        # Create a dict with ID as key and shape data entry as value
        for shape in shapes:
            self._init_dict_by_id(shape)

    def get_shape_coords_by_id(self, shape_id: int) -> List[Tuple[float, float]]:
        """
        Get a list of :class:`MMTShapes` by ``shape_id``.

        :raise ShapeIdNotFoundError: if `shape_id` is not in the loaded data
        """
        if shape_id not in self._dict_by_id:
            raise ShapeIdNotFoundError(shape_id)

        return [shape.coordinate for shape in self._dict_by_id[shape_id]]

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTShape.parse_from_row(row)
