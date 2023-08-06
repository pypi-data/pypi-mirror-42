import prometheus_client  # type: ignore
import pytest  # type: ignore
from aiohttp import web

from aiohttp_metrics import setup as setup_metrics


async def test_set_app_name():
    app = web.Application()

    with pytest.raises(AssertionError):
        setup_metrics(app)


async def test_setup_handler():
    app = web.Application()
    app['app_name'] = 'foo'
    setup_metrics(app)

    assert 'metrics' in app.router.named_resources()
    assert str(app.router.named_resources()['metrics'].url_for()) == '/-/metrics'


async def test_default_metrics(aiohttp_client):
    app = web.Application()
    app['app_name'] = 'foo'
    setup_metrics(app)

    client = await aiohttp_client(app)

    url = app.router.named_resources()['metrics'].url_for()
    resp = await client.get(url)
    data = await resp.text()

    assert resp.headers['Content-Type'] == prometheus_client.CONTENT_TYPE_LATEST

    assert 'requests_total' in data
    assert 'requests_latency_seconds' in data
    assert 'requests_in_progress_total' in data


async def test_add_custom_metrics(aiohttp_client):
    app = web.Application()
    app['app_name'] = 'foo'

    metric = prometheus_client.Counter(
        'users_registered', 'Total registered users count'
    )
    setup_metrics(app, metrics={
        'users_registered': metric
    })

    assert 'users_registered' in app['metrics']

    client = await aiohttp_client(app)

    url = app.router.named_resources()['metrics'].url_for()
    resp = await client.get(url)
    data = await resp.text()

    assert 'users_registered' in data
