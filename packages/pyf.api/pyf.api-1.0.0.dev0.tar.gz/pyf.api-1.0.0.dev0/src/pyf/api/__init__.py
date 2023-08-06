# -*- coding: utf-8 -*-
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config_params = {"settings": settings}
    config = Configurator(**config_params)
    config.include("cornice")
    config.scan()
    return config.make_wsgi_app()
