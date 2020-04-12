import os
from unittest.mock import Mock

from django.conf import settings
import django_rq

import pytest_django_rq.django_rq_worker as M  # noqa: F401

mock = Mock()


def background_func(foo, bar):
    mock()


def test_work_should_consume_jobs(django_rq_worker, mocker):
    settings.configure(
        DEBUG=True,
        # settings copied from django_rq's README
        INSTALLED_APPS=(
            # other apps
            "django_rq",
        ),
        RQ_QUEUES={
            'default': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
                'PASSWORD': 'some-password',
                'DEFAULT_TIMEOUT': 360,
            },
            'with-sentinel': {
                'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
                'MASTER_NAME': 'redismaster',
                'DB': 0,
                'PASSWORD': 'secret',
                'SOCKET_TIMEOUT': None,
                'CONNECTION_KWARGS': {'socket_connect_timeout': 0.3},
            },
            'high': {
                'URL': os.getenv(
                    'REDISTOGO_URL', 'redis://localhost:6379/0'
                ),  # If you're on Heroku
                'DEFAULT_TIMEOUT': 500,
            },
            'low': {'HOST': 'localhost', 'PORT': 6379, 'DB': 0},
        },
    )

    django_rq.enqueue(background_func, 'foo', bar='baz')
    mock.assert_not_called()

    django_rq_worker.work()

    mock.assert_called()
