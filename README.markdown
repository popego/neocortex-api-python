# Meaningtool Neocortex Python Client project

This is a library that implements [meaningtool's neocortex API](http://www.meaningtool.com/developers/docs/api/rest/v0.2) in python.

All API access begins with the creation of a `NeocortexRestClient` object.  For the sake of brevity, this document assumes you've created an object called `nc` as a meaningtool endpoint:
	
    nc = neocortex_client.NeocortexRestClient(<api_key>)
