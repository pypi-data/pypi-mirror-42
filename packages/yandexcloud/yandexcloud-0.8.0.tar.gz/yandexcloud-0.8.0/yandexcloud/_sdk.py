import inspect
import grpc

from yandexcloud import _channels
from yandexcloud import _operation_waiter


class SDK(object):
    def __init__(self, interceptor=None, **kwargs):
        self._channels = _channels.Channels(**kwargs)
        self._default_interceptor = interceptor

    def set_interceptor(self, interceptor):
        self._default_interceptor = interceptor

    def client(self, stub_ctor, interceptor=None):
        service = _service_for_ctor(stub_ctor)
        channel = self._channels.channel(service)
        if interceptor is not None:
            channel = grpc.intercept_channel(channel, interceptor)
        elif self._default_interceptor is not None:
            channel = grpc.intercept_channel(channel, self._default_interceptor)
        return stub_ctor(channel)

    def waiter(self, operation_id):
        return _operation_waiter.operation_waiter(self, operation_id, timeout=None)


def _service_for_ctor(stub_ctor):
    m = inspect.getmodule(stub_ctor)
    name = m.__name__
    if not name.startswith('yandex.cloud'):
        raise RuntimeError('Not a yandex.cloud service {}'.format(stub_ctor))

    for k, v in _supported_modules.items():
        if name.startswith(k):
            return v

    raise RuntimeError('Unknown service {}'.format(stub_ctor))


_supported_modules = {
    'yandex.cloud.compute': 'compute',
    'yandex.cloud.endpoint': 'endpoint',
    'yandex.cloud.iam': 'iam',
    'yandex.cloud.mdb.clickhouse': 'mdb-clickhouse',
    'yandex.cloud.mdb.mongodb': 'mdb-mongodb',
    'yandex.cloud.mdb.postgresql': 'mdb-postgresql',
    'yandex.cloud.operation': 'operation',
    'yandex.cloud.resourcemanager': 'resourcemanager',
    'yandex.cloud.vpc': 'vpc',
}
