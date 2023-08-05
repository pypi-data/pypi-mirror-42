=============================
Centreon SDK Python
=============================

.. image:: https://badge.fury.io/py/centreonapi.png
    :target: http://badge.fury.io/py/centreonapi

.. image:: https://travis-ci.com/guillaumewatteeux/centreon-sdk-python.svg?branch=dev
    :target: https://travis-ci.org/guillaumewatteeux/centreon-sdk-python

Make a Python LIB for Centreon API

Forked from https://github.com/centreon/centreon-sdk-python

Usages
------

* Connect to Centreon platform

.. code-block:: python

    from centreonapi.centreon import Webservice
    centreon = centreon("https://centreon.mydomain.tld, "admin", "centreon")

* List all hosts on Centreon platform

.. code-block:: python

    centreon.hosts.list()
    >>>
    {
      'Centeon-central': Centeon-central,
      'server1': myserver1
    }


* Add new host

.. code-block:: python

    centreon.hosts.add(
      name='server1',
      alias='DBServ',
      ip=127.0.0.1,
      template="DB-Host-Template",
      hg="DB Servers"
      )

* Get host

.. code-block:: python

    _, myhost = centreon.hosts.get('server1')
    myhost.name
    >>>
    server1

* Macros

Get macros

.. code-block:: python

    _, macros = myhost.getmacro()
    macros
    >>>
    {
      '$_HOSTMODULESTATSFILE$': $_HOSTMODULESTATSFILE$,
      '$_HOSTMYSQLPASSWORD$': $_HOSTMYSQLPASSWORD$,
      '$_HOSTMYSQLPORT$': $_HOSTMYSQLPORT$,
    }

    mymacro = macros.get('$_HOSTMYSQLPORT$')
    mymacro.value
    >>>
    3306

Set Macros

.. code-block:: python

    myhost.setmacro('SECRETMACRO', 'pass', 1, 'secret macro pass')

* HostTemplate on host

.. code-block:: python

    myhost.gettemplate()
    >>>
    {
      'App-Monitoring-Centreon-Central-custom': App-Monitoring-Centreon-Central-custom,
      'App-Monitoring-Centreon-Database-custom': App-Monitoring-Centreon-Database-custom,
      'App-Monitoring-Centreon-Poller-custom': App-Monitoring-Centreon-Poller-custom
    }


Features
--------

* TODO

