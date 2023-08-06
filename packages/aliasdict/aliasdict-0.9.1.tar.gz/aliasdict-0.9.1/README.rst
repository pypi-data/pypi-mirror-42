================
CacheLite
================

Documentation
-------------

The full documentation is at https://cachelite.readthedocs.org/

Quickstart
----------

Install cachelite::

    pip install aliasdict

Then you can use it.

.. code-block:: python

    import aliasdict from AliasDict

    adct = AliasDict()

    #put a key-value
    adct["YOUR_KEY"] = "YOUR_VALUE"

    #set a alias to key
    adct.set_alias("YOUR_KEY", "YOUR_ALIAS")

    #get value by alias
    adct["YOUR_ALIAS"]


