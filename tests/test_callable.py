from typing import Callable

import pytest

from pydantic import BaseModel, ValidationError


@pytest.mark.parametrize('annotation', [Callable, Callable[[int], int]])
def test_callable(annotation):
    class Model(BaseModel):
        callback: annotation

    m = Model(callback=lambda x: x)
    assert callable(m.callback)


@pytest.mark.parametrize('annotation', [Callable, Callable[[int], int]])
def test_non_callable(annotation):
    class Model(BaseModel):
        callback: annotation

    with pytest.raises(ValidationError):
        Model(callback=1)


@pytest.mark.parametrize('annotation', [Callable[[None], None], Callable[[int], int]])
def test_callable_one_param(annotation):
    class Model(BaseModel):
        callback: annotation

    m = Model(callback=lambda x: x)
    assert callable(m.callback)

    with pytest.raises(ValidationError):
        m = Model(callback=lambda x, y: None)

    with pytest.raises(ValidationError):
        m = Model(callback=lambda : None)
