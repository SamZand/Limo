# pylint: disable=import-error
import lemonator

def test_version():
    assert lemonator.__version__ == "0.0.1"

def test_add():
    assert lemonator.add(1, 2) == 3

def test_subtract():
    assert lemonator.subtract(1, 2) == -1
