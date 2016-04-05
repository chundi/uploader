# -*- coding:utf-8 -*-

from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('upload_token', '/upload_token')
    config.add_route('file', '/file')
    config.scan()
    return config.make_wsgi_app()

