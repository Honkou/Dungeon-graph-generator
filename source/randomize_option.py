"""Module containing randomizing function."""

import random
from collections.abc import Callable
from typing import Any


def randomize_function(
    popular_function: Callable,
    unlikely_function: Callable,
    chance: int,
    *args: Any,  # noqa: ANN401
    **kwargs: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    """Randomize between using first or second function.

    The chance indicates a chance one in x of using the second function instead of the first one.
    """
    roll = random.randint(1, chance)
    if roll == chance:
        return unlikely_function(*args, **kwargs)
    return popular_function(*args, **kwargs)
