================
CacheLite
================


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

    #save1
    with open( "PATH_TO_FILE", "wb") as f:
        adct.dump(f)

    #save2
    with open( "PATH_TO_FILE", "wb") as f:
        f.write(adct.dumps())


    #load1
    with open( "PATH_TO_FILE", "rb") as f:
        adct = AliasDict.load(f)

    #load2
    with open( "PATH_TO_FILE", "rb") as f:
        adct = AliasDict.loads(f.read())


