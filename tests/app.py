from unittest.mock import Mock
from django_rq import job

mock = Mock()


def background_func(foo, bar):
    mock()


@job
def decorated_background_func():
    mock()
