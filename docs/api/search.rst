.. _api_search:

Search (Deprecated)
===================

.. note::
    Please use the :ref:`api_geolocate_latest` API instead.

Purpose
    Determine the current location based on provided data about nearby
    cell or WiFi networks.


Request
-------

Search requests are submitted using a POST request to the URL::

    https://location.services.mozilla.com/v1/search?key=<API_KEY>

A search record can contain a list of cell records and a list of WiFi
records.

A example of a well formed JSON search request :

.. code-block:: javascript

    {
        "radio": "gsm",
        "cell": [
            {
                "radio": "umts",
                "mcc": 123,
                "mnc": 123,
                "lac": 12345,
                "cid": 12345,
                "signal": -61,
                "asu": 26
            }
        ],
        "wifi": [
            {
                "key": "01:23:45:67:89:ab",
                "channel": 11,
                "frequency": 2412,
                "signal": -50
            },
            {
                "key": "01:23:45:67:ab:cd"
            },
            {
                "key": "01:23:45:67:cd:ef"
            }
        ]
    }


Field Definition
----------------

Cell Fields
~~~~~~~~~~~

radio
    The type of radio network. One of `gsm`, `umts`, `lte` or `cdma`.

mcc
    The mobile country code. For CMDA networks it is not defined.
    If the device is a combined GSM/CDMA phone, the GSM mobile country
    code might be available and used for the CDMA network.

mnc
    The mobile network code or the system id for CDMA networks.

lac
    The location area code for GSM and WCDMA networks. The tracking area
    code for LTE networks. The network id for CDMA networks.

cid
    The cell id or cell identity. The base station id for CDMA networks.

psc
    The primary scrambling code for WCDMA and physical cell id for LTE.

signal
    The signal strength for this cell network, either the RSSI or RSCP.

ta
    The timing advance value for this cell network.


WiFi Fields
~~~~~~~~~~~

For `wifi` entries, the `key` field is required. The client must check the
Wifi SSID for a `_nomap` suffix. Wifi networks with such a suffix must not be
submitted to the server.

Most devices will only report the WiFi frequency or the WiFi channel,
but not both. The service will accept both if they are provided,
but you can include only one or omit both fields.

key **(required)**
    The client must check the WiFi SSID for a `_nomap`
    suffix. WiFi networks with such a suffix must not be submitted to the
    server. WiFi networks with a hidden SSID should not be submitted to the
    server either.

    The `key` is the BSSID of the WiFi network. So for example
    a valid key would look similar to `01:23:45:67:89:ab`.

frequency
    The frequency in MHz of the channel over which the client is
    communicating with the access point.

channel
    The channel is a number specified by the IEEE which represents a
    small band of frequencies.

signal
    The received signal strength (RSSI) in dBm, typically in the range of
    -51 to -113.

signalToNoiseRatio
    The current signal to noise ratio measured in dB.

An example of a valid WiFi record is below:

.. code-block:: javascript

    {
        "key": "01:23:45:67:89:ab",
        "channel": 11,
        "frequency": 2412,
        "signal": -51,
        "signalToNoiseRatio": 37
    }


Mapping records into a search request
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The mapping can contain zero or more WiFi records and zero or more
cell records. If either list of records is empty, it can be omitted entirely.

For WiFi lookups you need to provide at least two WiFi keys of
nearby WiFi networks. This is an industry standard that is meant to
prevent you from looking up the position of a single WiFi over time.


Response
--------

A successful response will be:

.. code-block:: javascript

    {
        "status": "ok",
        "lat": -22.7539192,
        "lon": -43.4371081,
        "accuracy": 100
    }

The latitude and longitude are numbers, with seven decimal places of
actual precision. The coordinate reference system is WGS 84. The accuracy
is an integer measured in meters and defines a circle around the location.

Should the response be based on a GeoIP estimate:

.. code-block:: javascript

    {
        "status": "ok",
        "lat": 51.0,
        "lon": -0.1,
        "accuracy": 600000,
        "fallback": "ipf"
    }

Alternatively the fallback field can also state `lacf` for an estimate
based on a cell location area.

If no position can be determined, you instead get:

.. code-block:: javascript

    {
        "status": "not_found"
    }
