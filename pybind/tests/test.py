# pylint: disable=import-error
# pep8: disable=E223
import lemonator

def test_version():
    assert lemonator.__version__ == "0.0.1"

def test_update():
    lemonator.update()