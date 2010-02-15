# Meaningtool Neocortex API Python Client

This is a library that implements [meaningtool's neocortex API][apidocs] in python.

All API access begins with the creation of a `NeocortexRestClient` object.  For the sake of brevity, this document assumes you've created an object called `nc` as a meaningtool endpoint:
	
    from neocortex.client import NeocortexRestClient
    nc = NeocortexRestClient('myapikey')

You can find your api key from your account page at [meaningtool](http://www.meaningtool.com).

Wherever you are asked for input on neocortex's API mehtods it can either be an url or text.

## Categories

Obtain a set of categories of an specific tree from your input.

    ca = nc.categories('yourinput', 'sometreekey')

You can pick a tree to categorize your input from the [public tree directory][treedirectory] or from your private trees on your 'My Trees' section at [meaningtool][meaningtool], by pasting the desired tree's key.

Some examples for better understanding:

    # This example uses the default 'General Knowledge' tree.
    ca = nc.categories('http://news.bbc.co.uk/2/hi/science/nature/8414798.stm')

    # This example uses the 'Gadget Trends' tree.
    ca = nc.categories('http://www.wired.com/gadgetlab/2009/12/apple-live-video/', '7fdc08c2-37e8-46a6-b8db-27e328d47320')

## Keywords

Obtain a set of keywords from your input.

    kw = nc.keywords('yourinput')

## Entities

Obtain a set of entities from your input.

    en = nc.entities('yourinput')

## Language

Obtain your input's language.

    la = nc.language('yourinput')

## Multifunction Requests

You can use this feature to obtain results of multiple api methods for the same input in one request.

You must first get a builder:

    builder = nc.get_builder()
    
Then you can chain any api method, for example:

    res = builder.input('yourinput').categories().keywords().language().meaningfy()

Obtaining your result from `res.payload`.

[meaningtool]: http://www.meaningtool.com
[apidocs]: http://www.meaningtool.com/developers/docs/api/rest/v0.2
[treedirectory]: http://www.meaningtool.com/developers/directory

