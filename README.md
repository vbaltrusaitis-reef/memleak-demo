# Memory leak

This is a minimal demo that shows a memory leak that happens due to [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) under very particular conditions. The problem may be related to https://github.com/jazzband/django-debug-toolbar/issues/906.

## Conditions

You can see files `requirements.txt`, `settings.py` and `urls.py` to see comments showing which code changes result in eliminating the leak.

1. We import `debug_toolbar` module in `urls.py`. This causes the leak even when `debug_toolbar` is never used and `DEBUG`, `DEBUG_TOOLBAR` are set to `False` in `settings.py`.

2. `django-debug-toolbar` is version `3.2.4`. If we use `3.5.0`, the leak doesn't happen.

3. We use `channels_redis.core.RedisChannelLayer`. If we use `channels.layers.InMemoryChannelLayer`, the leak doesn't happen.

4. We call `RedisChannelLayer.group_send()` method in a view.

5. We set up the root logger to use `DEBUG` level. If it's `INFO`, the leak doesn't happen.

6. We run the app with `gunicorn`. If we run the app using Daphne or hypercorn with ASGI interface, the leak doesn't happen.

## Running the test

1. `pip install -r requirements.txt`

2. `cd memtest`

3. Run a Redis instance.

4. `SECRET_KEY=<your_secret> REDIS_HOST=<your_redis_host> REDIS_PORT=<your_redis_port> gunicorn -w 1 memtest.wsgi:application`

5. In another terminal, run `while true; do curl localhost:8000/memory_leak; sleep 1; done` -- this will produce output that shows what additional objects were allocated (and not collected) after each call. Alternatively, just run `curl localhost:8000/memory_leak` continuously in a loop and see the gunicorn process memory grow.

## The fix

Either update `django-debug-toolbar` or import it only in `DEBUG = True` environments (which will still cause the leak in `DEBUG` mode, but `DEBUG` mode leaks memory regardless of using the toolbar).
