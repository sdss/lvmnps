.. _lvmnps-api:

API
===

Base client
-----------

.. autoclass:: lvmnps.nps.core.NPSClient
   :members:
   :show-inheritance:

.. autopydantic_model:: lvmnps.nps.core.OutletModel
   :model-show-json: false
   :exclude-members: model_post_init


Implementations
---------------

.. autoclass:: lvmnps.nps.implementations.dli.DLIClient

.. autopydantic_model:: lvmnps.nps.implementations.dli.DLIOutletModel
   :model-show-json: false
   :exclude-members: model_post_init


Tools
-----

.. automodule:: lvmnps.tools
