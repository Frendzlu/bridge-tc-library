try:
    from .strategy import MovementStrategy  # type: ignore
except Exception:
    MovementStrategy = None  # type: ignore

try:
    from .abstract_rotation import AbstractRotation  # type: ignore
except Exception:
    RotationCalculator = None  # type: ignore

try:
    from .movement import BaseMovement  # type: ignore
except Exception:
    BaseMovement = None  # type: ignore

__all__ = [
    name for name in (
        'MovementStrategy', 'RotationCalculator', 'BaseMovement'
    ) if name in globals() and globals()[name] is not None
]

