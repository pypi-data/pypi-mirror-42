===========================
cimpress-tagliatelle-python
===========================

Package that provides reusable code that makes it easy to access Tagliatelle tags in python projects.

Usage
-----

This package provides both high level and low level client.

High level client focuses on abstracting the operation

* for example fetching tags for any combination of resource and tag urn:

.. code-block:: python

    from tagliatelle.Client import Client

    client = Client(bearer, None)
    bulkResponse = client.tag().with_key("urn:space").fetch()
    for response in bulkResponse.results:
       print (f'{response.resourceUri} -> {response.value}')

* removing tags for any combination of tag urn and resource uri:

.. code-block:: python

    from tagliatelle.Client import Client

    client = Client(bearer, None)
    bulkResponse = client.tag().with_key("urn:space").remove()

* or create / update

.. code-block:: python

    from tagliatelle.Client import Client

    client = Client(bearer, None)
    bulkResponse = client.tag().with_key("urn:space").with_resource("http://some.resource.url").with_string_value("tag value").apply()


The low level client is exposing granular operations exsposed by Tagliatelle API

* get_tags
* post_tag
* put_tag
* delete_tag