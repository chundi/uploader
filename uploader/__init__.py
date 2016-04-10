# -*- coding:utf-8 -*-

import sys
from pyramid.config import Configurator

reload(sys)
sys.setdefaultencoding('utf-8')

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('log', '/log')
    config.scan()
    return config.make_wsgi_app()

