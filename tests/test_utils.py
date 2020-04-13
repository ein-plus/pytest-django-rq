import pytest_django_rq.utils as M


def test_extract_args_should_return_args_passed_in():
    def f(host='localhost', port=8888, retry=3):
        pass

    args = M.extract_args(f, ('host', 'port'), port=8000)
    assert args == ('localhost', 8000)
