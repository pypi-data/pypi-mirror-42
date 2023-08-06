aiohttp_metrics
===============
.. image:: https://travis-ci.com/clayman74/aiohttp-metrics.svg?branch=master
    :target: https://travis-ci.com/clayman74/aiohttp-metrics
.. image:: https://badge.fury.io/py/aiohttp_metrics.svg
    :target: https://badge.fury.io/py/aiohttp_metrics

The library provides expose Prometheus metrics for `aiohttp.web`__-based applications.

.. _aiohttp_web: http://aiohttp.readthedocs.org/en/latest/web.html

__ aiohttp_web_


Installation
------------

    $ pip install aiohttp_metrics


Usage
-----

The library allows us to expose application metrics,
like number of served requests and requests latency, for Prometheus monitoring.

Before exposing the metrics, you have to add `app_name` and register the
*metrics middleware* and *metrics handler* in ``aiohttp.web.Application``.


A trivial usage example:

.. code:: python

    from aiohttp import web
    from aiohttp_metrics import setup as setup_metrics


    async def handler(request):
        return web.Response(text='Hello world')


    def make_app():
        app = web.Application()
        app['app_name'] = 'foo'

        setup_metrics(app)
        app.router.add_get('/', handler)
        return app


    web.run_app(make_app())

Now you can access your metrics on `http://localhost:8080/-/metrics`.
Path could by changed by `path` parameter in `setup`.

You can also specify you custom metrics:

.. code:: python

    import prometheus_client
    from aiohttp import web
    from aiohttp_metrics import setup as setup_metrics


    async def handler(request):
        request.app['metrics']['foo'].labels(request.app['app_name']).inc()
        return web.Response(text='Hello world')


    def make_app():
        app = web.Application()
        app['app_name'] = 'foo'

        setup_metrics(app, metrics={
            'foo': prometheus_client.Counter(
                'foo', 'Foo counter', ('app_name', )
            )
        })

        app.router.add_get('/', handler)

        return app


    web.run_app(make_app())


Developing
----------

Install for local development::

    $ flit install -s

Run tests with::

    $ tox


License
-------

``aiohttp_metrics`` is offered under the MIT license.
