# Memory leak conditions

The leak happens when _all_ af these conditions are present:

1. We use `channels_redis.core.RedisChannelLayer`. The leak doesn't happen with `channels.layers.InMemoryChannelLayer`.

2. We call `RedisChannelLayer.group_send` in a view.

3. We import `debug_toolbar` module in `urls.py`. This causes the leak even when `debug_toolbar` is never used and `DEBUG`, `DEBUG_TOOLBAR` are set to `False` in `settings.py`.

4. `django-debug-toolbar` is version `3.2.4`. Updating to `3.5.0` solved the problem.

5. We set up the root logger to use `DEBUG` level. If it's `INFO`, the leak doesn't happen.

6. We run the app with `gunicorn`. Running Daphne or hypercorn with ASGI interface removes the problem.

# Running the test

1. `pip install -r requirements.txt`

2. `cd memtest`

3. `SECRET_KEY="your_secret" REDIS_HOST=localhost REDIS_PORT=8379 gunicorn -w 1 memtest.wsgi:application`

4. In another terminal, run `while true; do curl localhost:8000/memory_leak; sleep 1; done` -- this will produce output that shows what additional objects were allocated after each call. Alternatively, just run `curl localhost:8000/memory_leak` continuously in a loop and see the gunicorn process memory grow.

# The fix

Either update `django-debug-toolbar` or import it only in `DEBUG = True` environments.