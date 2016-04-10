# -*- coding:utf-8 -*-

from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('log', '/log')
    config.scan()
    return config.make_wsgi_app()

