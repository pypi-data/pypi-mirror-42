microhttp-ratelimit
===================

Rate limit extension for microhttp

- Based LeakyBucket method on Redis
- IP throttler decorator


Install
-------


.. code-block:: bash

    pip install microhttp-ratelimit

Note: required to install ``Redis``.


Configuration
-------------

.. code-block:: yaml

    rate_limit:
      namespace_prefix: myApp
      redis:
        host: localhost
        port: 6379
      ip_rules:
        default:
          period: 900 # 15 Minutes
          limit: 180
        slow:
          period: 86400 # 24 Hours
          limit: 50
        very_slow:
          period: 86400
          limit: 10
