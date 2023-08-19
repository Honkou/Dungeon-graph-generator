"""Tests for randomize_option.py."""

from unittest.mock import patch

from source.randomize_option import Function, randomize_function


def popular_func() -> str:
    """Return a str for a quick call assetion."""
    return "The likely dummy function was called."


def unpopular_func() -> str:
    """Return a str for a quick call assetion."""
    return "The lucky dummy function was called."


def test_function_class_init():
    """Assert correct Function object creation."""
    fake_func = print
    fake_args = ("first arg", 2)
    fake_kwargs = {"first_kwarg": 1}
    fake_function_obj = Function(fake_func, fake_args, fake_kwargs)
    assert fake_function_obj.function == fake_func
    assert fake_function_obj.args == fake_args
    assert fake_function_obj.kwargs == fake_kwargs


def test_function_class_call():
    """Assert the Callable in the class is being called correctly."""
    with patch("builtins.print") as mocked_print:
        fake_func = print
        fake_args = ("first arg", 2)
        fake_kwargs = {"first_kwarg": 1}
        fake_function_obj = Function(fake_func, fake_args, fake_kwargs)
        fake_function_obj.call()
        mocked_print.assert_called_once_with(*fake_args, **fake_kwargs)


def test_popular_function_call():
    """Assert that the popular function is called when the stars don't align."""
    with patch("random.randint") as fake_random:
        fake_random.return_value = 1
        tested_value = randomize_function(Function(popular_func), Function(unpopular_func), chance=2)
        assert tested_value == "The likely dummy function was called."


def test_unpopular_function_call():
    """Assert that the unpopular function is called when the stars align."""
    with patch("random.randint") as fake_random:
        fake_random.return_value = 2
        tested_value = randomize_function(Function(popular_func), Function(unpopular_func), chance=2)
        assert tested_value == "The lucky dummy function was called."
