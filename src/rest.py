import re
import urllib
import urllib2

try:
    import json
except ImportError:
    import simplejson as json


_re_url = re.compile(ur"^https?://.+$")


###############################################################################
## Exceptions
###############################################################################

class MeaningtoolError(Exception):
    message = u"An error ocurred with the requested resource."

class ResponseBodyFormatNotValid(MeaningtoolError):
    message = u"The response body is not in the expected format."
    
class InvalidParameter(MeaningtoolError):
    """ 
    Exception raised when a parameter of the client had an invalid value.
    """
    message = u"A parameter has an invalid value."

class InvalidUrl(InvalidParameter):
    """ 
    Exception raises when a url is invalid. This can be happen
    on two situations:
        - the input is an url.
        - the `url_hint` parameter was used.
    """
    message = u"The url is invalid."


###############################################################################
## Response formats, parsers and Result classes
###############################################################################

class Result(object):
    """
    A unified access to the retrieved API results
    """
    def __init__(self, status_code, status_message, payload=None, metadata=None):
        """
        Creates the result.
        
        :parameters:
            status_code: str
                the status of the response.
            status_message: str
                the message of the response.
            payload: dict()
                the payload data of the response.
        """
        self.code = status_code
        self.message = status_message
        self.payload = payload
        self.metadata = metadata or {}
        
    def __repr__(self):
        return u"<%s - %s>" % (self.__class__.__name__, self.message)
    
    
class ResponseParser(object):
    """
    Responsible for parse the raw API response
    """
    result_class = None
    available_exceptions = None
    
    def __init__(self, result_class=None, available_exceptions=None):
        self.result_class = result_class or self.result_class or Result
        self.available_exceptions = available_exceptions or self.available_exceptions or []
    
    def parse(self, raw):
        raise NotImplementedError("'parse' method must be implemented.")
    
    def _parse_dict(self, rdict):
        status = rdict["status"]
        message = rdict["message"]
        code = rdict["code"]
        payload = rdict.get("payload", None)
        metadata = rdict.get("metadata", None)
        
        if status == "ok":
            if self.result_class is not None:
                return self.result_class(code, message, payload, metadata)
            else:
                return (code, message, payload, metadata)
        else:
            raise MeaningtoolError(message)
            
    def _raise_exception_from_code(self, code):
        if self.available_exceptions is None:
            raise MeaningtoolError()
        
        for exception in self.available_exceptions:
            if (hasattr(exception, "code") and code == exception.code) \
                or (hasattr(exception, "get_code") and code == exception.get_code()) \
                or exception.__name__ == code:
                raise exception()
            
        raise MeaningtoolError()

class RawResponseParser(ResponseParser):
    def parse(self, raw):
        return raw

class XmlResponseParser(ResponseParser):
    def parse(self, raw):
        return raw
    
class JsonResponseParser(ResponseParser):
    def parse(self, raw):
        try:
            d = json.loads(raw, encoding="utf8")
        except:
            raise ResponseBodyFormatNotValid()
        return self._parse_dict(d)

class ResponseFormats(object):
    XML = "xml"
    JAVASCRIPT = "js"
    JSON = "json"



###############################################################################
## Base Rest Client
###############################################################################

class RestClient(object):
    
    POSIBLE_HTTP_CODES = [400, 401, 403, 404, 409, 500]
    
    base_url = None
    api_key = None
    result_class = None
    available_exceptions = None
    parsers_map = None
    
    _response_format = ResponseFormats.JSON
    

    def __init__(self, base_url=None, api_key=None, result_class=None, available_exceptions=None, parsers_map=None,):
        self.base_url = base_url or self.base_url
        self.api_key = api_key or self.api_key
        if parsers_map is None and self.parsers_map is None:
            self.result_class = result_class or self.result_class or Result
            self.available_exceptions = available_exceptions or self.available_exceptions
            self.parsers_map = {
                "xml":XmlResponseParser(self.result_class, self.available_exceptions),
                "js": RawResponseParser(self.result_class, self.available_exceptions),
                "json": JsonResponseParser(self.result_class, self.available_exceptions)
            }
        else:
            self.parsers_map = parsers_map

    def get(self, url, data=None, headers=None, response_format=ResponseFormats.JSON):
        url = self._get_full_url(url)
        self._response_format = response_format
        return self._req("GET", url, data, headers)

    def post(self, url, data=None, headers=None, response_format=ResponseFormats.JSON):
        url = self._get_full_url(url)
        self._response_format = response_format
        return self._req("POST", url, data, headers)

    def put(self, url, data=None, headers=None, response_format=ResponseFormats.JSON):
        url = self._get_full_url(url)
        data = data or {}
        data['_method'] = 'PUT'
        self._response_format = response_format
        return self._req("POST", url, data, headers)

    def delete(self, url, data=None, headers=None, response_format=ResponseFormats.JSON):
        url = self._get_full_url(url)
        data = data or {}
        data['_method'] = 'DELETE'
        self._response_format = response_format
        return self._req("POST", url, data, headers)

    def _req(self, method, url, data=None, headers=None):
        headers = headers or []
        data = data or {}
        data['api_key'] = self.api_key

        # validate url
        if not _re_url.match(url):
            raise InvalidUrl(url)
        
        # validate method
        if method == "GET":
            req = urllib2.Request(u"%s?%s" % (url, urllib.urlencode(data)))
        elif method == "POST":
            req = urllib2.Request(url, urllib.urlencode(data))
        else:
            raise ValueError(u"HTTP Method '%s' not supported" % method)
        
        if self._response_format == ResponseFormats.JSON:
            req.add_header("Accept", "application/json")
        elif self._response_format == ResponseFormats.JAVASCRIPT:
            req.add_header("Accept", "application/javascript")
        elif self._response_format == ResponseFormats.XML:
            req.add_header("Accept", "application/xml")
            
        req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.add_header("Accept-Charset", "UTF-8")
        for k,v in headers:
            req.add_header(k, v)
        
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            if e.code not in self.POSIBLE_HTTP_CODES:
                raise BaseRestClientError("There was an error while getting the data.")
            resp = e
        
            if resp.headers.gettype() == "text/plain":
                raise ValueError(resp.read())
        
        parser = self.parsers_map.get(self._response_format, RawResponseParser())
        return parser.parse(resp.read())
    
    def _get_full_url(self, url):
        if not self.base_url.endswith("/"):
            self.base_url = "%s/" % self.base_url
        if url.startswith("/"):
            url = url[1:]
        return "%s%s" % (self.base_url, url)
