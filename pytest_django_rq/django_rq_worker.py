import logging

from django_rq import get_worker
from rq.worker import SimpleWorker
import fakeredis
import pytest

from .utils import memorize

logger = logging.getLogger(__name__)


@memorize(key_params=('host', 'port'))
def fake_server(host='localhost', port=6379, *args, **kwargs):
    logger.debug("Create FakeServer for %s:%s", host, port)
    return fakeredis.FakeServer()


@pytest.fixture
def django_rq_worker(mocker):
    def fake_redis(*a, **kw):
        return fakeredis.FakeRedis(server=fake_server(*a, **kw))

    def fake_strict_redis(*a, **kw):
        return fakeredis.FakeStrictRedis(server=fake_server(*a, **kw))

    mock_redis = mocker.patch('redis.Redis', wraps=fakeredis.FakeRedis)
    mock_redis.side_effect = fake_redis
    mock_strict_redis = mocker.patch(
        'redis.StrictRedis', wraps=fakeredis.FakeStrictRedis
    )
    mock_strict_redis.side_effect = fake_strict_redis

    class Worker:
        @staticmethod
        def work():
            # Use SimpleWorker to avoid os.fork()
            get_worker(worker_class=SimpleWorker).work(burst=True)

    return Worker
