# pytest-django-rq


A pytest plugin to help writing unit test for django-rq.

This plugin provides a `django_rq_worker` fixture which has a `work()` method
to run all enqueued jobs in current process.


## Usage

```python
def test_async_api(django_rq_worker):
    client = django.test.Client()

    # Call an async API
    response = client.post(URL)
    assert response.status_code == 201  # Accepted

    # now let's run all enqueued jobs
    django_rq_worker.work()

    # assert the async jobs has taken place.
    assert ...
```
