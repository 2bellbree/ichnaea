.. _service_api:

============
Services API
============

The service APIs accept data submission for geolocation stumbling as well as
reporting a location based on IP addresses, cell, or WiFi networks.

New client developments should use the :ref:`api_region_latest`,
:ref:`api_geolocate_latest`, or :ref:`api_geosubmit_latest` APIs.

Requesting an API Key
=====================

The api key has a set daily usage limit of about 100,000 requests. As we aren't
offering a commercial service, please note that we do not make any guarantees
about the accuracy of the results or the availability of the service.

Please make sure that you actually need the raw API access to
perform geolocation lookups. If you just need to get location data
from your web application, you can directly use the
`HTML5 API
<https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/Using_geolocation>`_.

To apply for an API key, please
`fill out this form
<https://docs.google.com/forms/d/e/1FAIpQLSf2JaJm8V1l8TS_OiyjodkpYsagOhM1LNo_SmPDDAVKdmQg8A/viewform>`_.
When filling out the form, please make sure to describe your use-case and
intended use of the service. Our
`Developer Terms of Service
<https://location.services.mozilla.com/terms>`_ govern the use of MLS API keys.

We'll try to get back to you within a few days, but depending on vacation times
it might take longer.

API Access Keys
===============

.. Note::

   Mozilla is currently evaluating its MLS service and terms and is not
   currently distributing API keys.

You can anonymously submit data to the service without an API key via
any of the submission APIs.

You must identify your client to the service using an API key when
using one of the :ref:`api_region_latest` or :ref:`api_geolocate_latest` APIs.

If you want or need to specify an API key, you need to be provide
it as a query argument in the request URI in the form::

    https://location.services.mozilla.com/<API>?key=<API_KEY>

Each API key can be rate limited per calendar day, but the default is to allow
an unlimited number of requests per day.


Errors
======

Each of the supported APIs can return specific error responses. In addition
there are some general error responses.


Invalid API Key
---------------

If an API key was required but either no key was provided or the provided key
was invalid, the service responds with a ``keyInvalid`` message and HTTP 400
error code:

.. code-block:: javascript

    {
        "error": {
            "errors": [{
                "domain": "usageLimits",
                "reason": "keyInvalid",
                "message": "Missing or invalid API key."
            }],
            "code": 400,
            "message": "Invalid API key"
        }
    }


API Key Limit
-------------

API keys can be rate limited. If the limit for a specific API key is exceeded,
the service responds with a ``dailyLimitExceeded`` message and a HTTP 403
error code:

.. code-block:: javascript

    {
        "error": {
            "errors": [{
                "domain": "usageLimits",
                "reason": "dailyLimitExceeded",
                "message": "You have exceeded your daily limit."
            }],
            "code": 403,
            "message": "You have exceeded your daily limit."
        }
    }


Parse Error
-----------

If the client sends a malformed request, typically sending malformed or invalid
JSON, the service will respond with a ``parseError`` message and a HTTP 400
error code:

.. code-block:: javascript

    {
        "error": {
            "errors": [{
                "domain": "global",
                "reason": "parseError",
                "message": "Parse Error"
            }],
            "code": 400,
            "message": "Parse Error"
        }
    }


Service Error
-------------

If there is a transient service side problem, the service might respond with
HTTP 5xx error codes with unspecified HTTP bodies.

This might happen if part of the service is down or unreachable. If you
encounter any 5xx responses, you should retry the request at a later time. As a
service side problem is unlikely to be resolved immediately, you should wait a
couple of minutes before retrying the request for the first time and a couple
of hours later if there's still a problem.


APIs
====

Historically the service first offered the custom :ref:`api_search` and
:ref:`api_submit` APIs. Later it was decided to also implement the
:ref:`api_geolocate` API to lessen the burden on clients that want to
support multiple location services. As an extension to this the
:ref:`api_geosubmit` API was added to offer a consistent way to contribute
back data to the service. Afterwards the :ref:`api_region` API was added
and :ref:`api_geosubmit2` superseded its version 1 counterpart.

.. toctree::
   :maxdepth: 1

   geolocate
   region
   geosubmit2
   geosubmit
   search
   submit
