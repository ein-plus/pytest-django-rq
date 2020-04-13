import django_rq

import pytest_django_rq.django_rq_worker as M  # noqa: F401


def test_work_should_consume_jobs(django_rq_worker):
    from .app import mock, background_func

    mock.reset_mock()

    django_rq.enqueue(background_func, 'foo', bar='baz')
    mock.assert_not_called()

    django_rq_worker.work()

    mock.assert_called()


def test_should_support_job_decorator(django_rq_worker):
    from .app import mock, decorated_background_func

    mock.reset_mock()
    decorated_background_func.delay()
    mock.assert_not_called()
    django_rq_worker.work()
    mock.assert_called()
