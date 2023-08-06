# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def get_client(settings):
    """ES Client
    """
    return Elasticsearch(
        [{"host": settings["pyfapi.es.host"], "port": settings["pyfapi.es.port"]}]
    )


def get_search(settings):
    """ES DSL Search
    """
    return Search(using=get_client(settings), index=settings["pyfapi.es.index"])
