# -*- coding: utf-8 -*-
from collections import OrderedDict
from itertools import islice
from pyf.api.utils import get_search


def sort_on_score(search, order):
    return search.sort({"_score": order})


class Search(object):
    def __init__(self, settings, params, start, size):
        self.settings = settings
        self.params = params
        self.index = settings["pyfapi.es.index"]
        self.search = get_search(settings)
        self.start = start
        self.size = size

    def _build_search(self):
        search = self.search
        if self.params["classifiers"]:
            search = self.search.filter(
                "terms", **{"classifiers": self.params["classifiers"]}
            )
        if self.params["text"]:
            search = search.query(
                "multi_match",
                query=self.params["text"],
                fields=["name^1.2", "summary^1.1", "description"],
            )
            search = search.sort('_score')
        else:
            search = search.sort('name')
        return search

    def result(self):
        search = self._build_search()
        collector = OrderedDict()
        for hit in search.scan():
            if hit['name'] not in collector:
                collector[hit['name']] = hit
                continue
            existing = collector[hit['name']]
            if existing['version'] > hit['version']:
                collector[hit['name']] = hit
        result = {
            "total": len(collector),
            "start": self.start,
            "size": 0,
            "batch": [],
        }
        for name, hit in islice(collector.items(), self.start, self.start+self.size):
            result["batch"].append(hit.to_dict())
            result["size"] += 1
        return result
