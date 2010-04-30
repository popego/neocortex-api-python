# -*- coding: utf-8 -*-
__docformat__="restructuredtext"

from rest import RestClient, Result, ResponseFormats
from datetime import datetime
   

class NeocortexRestClient(object):
    BASE_URL = "http://api.meaningtool.com/0.2/neocortex"
    __builder__ = None
    
    class Builder(RestClient):
        _functions = {}
        _params = {}
        _input = None
        _format = None
        _tree_key = None
                
        def format(self, value):
            self._format = value
            return self
        
        def input(self, text):
            self._input = self._params["input"] = text
            return self
        
        def categories(self, tree_key=None, additionals=None):    
            params = dict(additionals or [])
            if tree_key is not None:
                params.update(dict(tree_key=tree_key))
            
            self._functions["categories"] = params
            return self
        
        def keywords(self):
            self._functions["keywords"] = True
            return self
        
        def entities(self):
            self._functions["entities"] = True
            return self
        
        def language(self):
            self._functions["language"] = True
            return self
        
        def meaningfy(self):
            fs = []
            for k,v in self._functions.items():
                kk = k
                if isinstance(v, dict):
                    if v.has_key("additionals"):
                        for a in v["additionals"]:
                            kk = "%s+%s" % (kk, a)
                    if v.has_key("tree_key") and v["tree_key"] is not None and kk == 'categories':
                        self._params["tree_key"] = v["tree_key"]
                fs.append(kk)
            fs = ";".join(fs)
            url = "%s.%s" % (fs, self._format)
            
            try:
                res = self.post(url, self._params, response_format=self._format)
            except Exception, e:
                raise e
            finally:
                self._reset()
                
            return res

        def _reset(self):
            self._functions = {}
            self._params = {}

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.BASE_URL = base_url or self.BASE_URL

    def get_builder(self):
        if self.__builder__ is None:
            self.__builder__ = NeocortexRestClient.Builder(self.BASE_URL, self.api_key).format(ResponseFormats.JSON)
            
        self.__builder__._reset()
        
        return self.__builder__

    def categories(self, input, tree_key=None, additionals=None):
        builder = self.get_builder()
        return builder.format(ResponseFormats.JSON).input(input).categories(tree_key, additionals).meaningfy().payload["categories"]

    def keywords(self, input):
        builder = self.get_builder()
        return builder.format(ResponseFormats.JSON).input(input).keywords().meaningfy().payload["keywords"]
        
    def entities(self, input):
        builder = self.get_builder()
        return builder.format(ResponseFormats.JSON).input(input).entities().meaningfy().payload["entities"]

    def language(self, input):
        builder = self.get_builder()
        return builder.format(ResponseFormats.JSON).input(input).language().meaningfy().payload["language"]
