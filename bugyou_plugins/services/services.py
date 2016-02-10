from importlib import import_module

from bugyou_plugins.services import ServiceProvider

SERVICES = {
    ServiceProvider.PAGURE:
    ('bugyou_plugins.services.pagure', 'PagureService'),
}

def get_service(service):
    if service in SERVICES:
        mod_name, driver_name = SERVICES[service]
        module = import_module(mod_name)
        return getattr(module, driver_name)
    raise AttributeError('Service %s does not exists' % [service])
