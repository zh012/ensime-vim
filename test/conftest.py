import os
import sys

import mock
import pytest

# pytest expects the project modules to be importable from whereever you run
# it, preferring that you do `pip install --editable .` -- we don't want to be
# a distributable Python package so this is easier than maintaining a useless
# setup.py.
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)


@pytest.fixture
def vim():
    """A wide-open mock vim object.

    We'll just have to be careful since we can't import a real vim object to
    use autospec and guarantee that we're calling real APIs.
    """
    return mock.NonCallableMock(name='mockvim')
