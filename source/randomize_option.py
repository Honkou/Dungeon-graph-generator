"""Module containing randomizing function."""

import random
from collections.abc import Callable
from typing import Any


class Function:

    """Represents a callable along with its arguments and keyword arguments."""

    def __init__(
        self,
        function: Callable,
        arguments: tuple = (),
        kw_arguments: dict | None = None,
    ) -> None:
        """Initialize the callable object."""
        if kw_arguments is None:
            kw_arguments = {}
        self.function = function
        self.args = arguments
        self.kwargs = kw_arguments

    def call(self) -> Any:  # noqa: ANN401
        """Call the function and return its results."""
        return self.function(*self.args, **self.kwargs)


def randomize_function(
    popular_function: Function,
    unlikely_function: Function,
    chance: int,
) -> Any:  # noqa: ANN401
    """Randomize between using first or second function.

    The chance indicates a chance one in x of using the second function instead of the first one.
    """
    roll = random.randint(1, chance)
    if roll == chance:
        return unlikely_function.call()
    return popular_function.call()
