limis
=====
.. image:: https://travis-ci.org/limis-project/limis.svg?branch=master
    :alt: limis build status
    :target: https://travis-ci.org/limis-project/limis

.. image:: https://codecov.io/gh/limis-project/limis/branch/master/graph/badge.svg
    :alt: limis coverage status
    :target: https://codecov.io/gh/limis-project/limis

limis is a light microservice framework built in `Python <https://www.python.org/>`_ and powered by
`Tornado <https://www.tornadoweb.org/>`_. The project is currently in active development and should be considered alpha
grade at the moment. Features are being added and removed and expect the API to change frequently.

Instructions
------------

Installation
~~~~~~~~~~~~
.. code-block::

    pip install limis

Project Creation
~~~~~~~~~~~~~~~~
.. code-block::

    limis-management create_project <project_name>

Service Creation
~~~~~~~~~~~~~~~~
.. code-block::

    cd <project_name>
    ./management create_service <service_name>

* Create your service components in '<service_name>/components.py'
* Add component classes to 'components' attribute of the service definition of '<service_name>/services.py'
* Add new service to the project services file '<project_name>/services.py'