import unittest
import urllib2

from rest import BaseRestClientError, UnknownException, ResponseBodyFormatNotValid, InvalidParameter, InvalidUrl
from neocortex.client import NeocortexRestClient
from base import data_response, fail_response

class NeocortexTest(unittest.TestCase):

    def setUp(self):
        self.client= NeocortexRestClient(u'APIKEY', u'TREEKEY')

    def test_input_missing(self):
        urllib2.urlopen= fail_response(BaseRestClientError)
        self.assertRaises(BaseRestClientError, self.client.categories, u'pepe')
        
    def test_short_input(self):
        pass
    
    def test_invalid_category_tree_key(self):
        pass
    
    def test_maintenance_category_tree(self):
        pass
    
    def test_invalid_url(self):
        pass
    
    def test_invalid_api_key(self):
        pass
    
    def test_api_limits_exceeded(self):
        pass
    
    
    
    def test_no_classifiers(self):
        urllib2.urlopen= fail_response(BaseRestClientError)
        self.assertRaises(BaseRestClientError, self.client.categories, u'pepe')

    def test_cannot_detect_lang(self):
        urllib2.urlopen= fail_response(BaseRestClientError)
        self.assertRaises(BaseRestClientError, self.client.categories, u'pepe')

    def test_data_response(self):
        data= {u'categories': [{u'score': 0.18388247648468797, u'name': u'Gaming'}, \
                               {u'score': 0.15857251730433639, u'name': u'Arts'}, \
                               {u'score': 0.16063399113213972, u'name': u'Lifestyle'}, \
                               {u'score': 0.26083577259764912, u'name': u'Movies'}]}
        
        urllib2.urlopen= data_response(data)
        result= self.client.categories(u'http://en.wikipedia.org/wiki/Angelina_Jolie')
        self.assertEqual(data, result.data)
