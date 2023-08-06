import time
from typing import Awaitable, Callable, Dict, Union

import prometheus_client  # type: ignore
from aiohttp import web
from prometheus_client import (
    CollectorRegistry, Counter, Enum, Gauge, Histogram, Info, Summary  # type: ignore
)


Handler = Callable[[web.Request], Awaitable[web.Response]]
Metric = Union[Counter, Gauge, Summary, Histogram, Info, Enum]


@web.middleware
async def middleware(request: web.Request, handler: Handler) -> web.Response:
    """
    Middleware to collect http requests count and response latency
    """

    start_time = time.monotonic()
    request.app['metrics']['requests_in_progress'].labels(
        request.app['app_name'], request.path, request.method).inc()

    response = await handler(request)

    resp_time = time.monotonic() - start_time
    request.app['metrics']['requests_latency'].labels(
        request.app['app_name'], request.path).observe(resp_time)
    request.app['metrics']['requests_in_progress'].labels(
        request.app['app_name'], request.path, request.method).dec()
    request.app['metrics']['requests_total'].labels(
        request.app['app_name'], request.method, request.path, response.status).inc()

    return response


async def handler(request: web.Request) -> web.Response:
    """
    Expose application metrics to the world
    """

    resp = web.Response(
        body=prometheus_client.generate_latest(
            registry=request.app['metrics_registry']
        )
    )

    resp.content_type = prometheus_client.CONTENT_TYPE_LATEST
    return resp


def setup(app: web.Application, *, path: str = '/-/metrics',
          metrics: Dict[str, Metric] = None) -> None:

    assert 'app_name' in app, 'Please set app name for metrics'

    app['metrics_registry'] = CollectorRegistry()
    app['metrics'] = {
        'requests_total': Counter(
            'requests_total', 'Total request count',
            ('app_name', 'method', 'endpoint', 'http_status'),
            registry=app['metrics_registry']
        ),
        'requests_latency': Histogram(
            'requests_latency_seconds', 'Request latency',
            ('app_name', 'endpoint'),
            registry=app['metrics_registry']
        ),
        'requests_in_progress': Gauge(
            'requests_in_progress_total', 'Requests in progress',
            ('app_name', 'endpoint', 'method'),
            registry=app['metrics_registry']
        )
    }

    if metrics:
        for key, metric in metrics.items():
            app['metrics'][key] = metric
            app['metrics_registry'].register(metric)

    app.middlewares.append(middleware)  # type: ignore

    app.router.add_get(path, handler, name='metrics')
