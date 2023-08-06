# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from pyf.api.search import Search
from pyf.api.views.base import Base
from pyf.api.views.base import CORS_POLICY
from pyf.api.views.base import PREFIX
from cornice.resource import resource

import logging

logger = logging.getLogger("pyf.api")


@resource(path=PREFIX + "/search", cors_policy=CORS_POLICY)
class SearchView(Base):
    def post(self):
        search_params = {}
        search_params["text"] = self.request.params.get("text", "")
        search_params["classifiers"] = self.request.params.getall("classifier")
        start = int(self.request.params.get("start", 0))
        size = int(self.request.params.get("size", 20))
        if size > 500:
            return self._error("Maximum batch size is 500!")
        try:
            search = Search(self.request.registry.settings, search_params, start, size)
            result = search.result()
        except Exception:
            logger.exception("Problem fetching result.")
            return self._error("Problem fetching result.")
        return self._result(result)
