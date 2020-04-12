import logging

from django_rq import get_worker
from rq.worker import SimpleWorker
import fakeredis
import pytest

from .utils import memorize

logger = logging.getLogger(__name__)


@memorize(key_params=('host', 'port', 'db'))
def fake_server(host='localhost', port=6379, db=0, *args, **kwargs):
    logger.debug("Create FakeServer for %s:%s/%s", host, port, db)
    return fakeredis.FakeServer()


@pytest.fixture
def django_rq_worker(mocker):
    def fake_redis(*a, **kw):
        return fakeredis.FakeStrictRedis(server=fake_server(*a, **kw))

    mocker.patch('redis.Redis').side_effect = fake_redis

    class Worker:
        @staticmethod
        def work():
            # Use SimpleWorker to avoid os.fork()
            get_worker(worker_class=SimpleWorker).work(burst=True)

    return Worker
