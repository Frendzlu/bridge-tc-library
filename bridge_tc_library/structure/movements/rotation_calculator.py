# python
import importlib
import inspect
from typing import Dict, Type, Any, Optional

from bridge_tc_library.structure import AbstractRotation


class RotationCalculator:
    """
    During initialization, dynamically imports all rotation classes from the
    'bridge_tc_library.structure.movements.rotations' module and stores them in a dictionary.
    """

    def __init__(self) -> None:
        module_name = "bridge_tc_library.structure.movements.rotations"
        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            raise ImportError(f"Couldn't import {module_name}: {e}") from e

        rotations: Dict[str, Type[Any]] = {}

        if hasattr(mod, "_rotation_classes") and isinstance(getattr(mod, "_rotation_classes"), dict):
            for name, cls in getattr(mod, "_rotation_classes").items():
                rotations[name] = cls
        else:
            for name in dir(mod):
                if name.startswith("_"):
                    continue
                attr = getattr(mod, name)
                if inspect.isclass(attr) and getattr(attr, "__module__", None) == mod.__name__:
                    rotations[name] = attr

        self.rotations = rotations

    def get(self, name: str):
        """Returns the rotation class by its name, or None if not found."""
        return self.rotations.get(name)

    def get_rotations(self, pairs: Optional[int] = None, boards_min: Optional[int] = None, boards_max: Optional[int] = None) -> \
    list[str] | None:
        """Returns a list of all available rotation names."""
        if pairs is None and boards_min is None and boards_max is None:
            return list(self.rotations.keys())
        if pairs is not None:
            raise NotImplementedError("Filtering by pairs is not implemented yet.")