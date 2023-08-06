========================================
Asynchronous server component library
========================================

.. image:: https://travis-ci.org/tangmi001/tomatolib.svg?branch=master
  :target: https://travis-ci.org/tangmi001/tomatolib
  :alt: Travis status for master branch

.. image:: https://codecov.io/gh/tangmi001/tomatolib/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/tangmi001/tomatolib
  :alt: Codecov

.. image:: https://img.shields.io/github/license/tangmi001/tomatolib.svg
  :target: https://github.com/tangmi001/tomatolib/blob/master/LICENSE
  :alt: License

.. image:: https://img.shields.io/pypi/v/tomatolib.svg
  :target: https://pypi.org/project/tomatolib
  :alt: PyPI


Features
========

- Manage common modules (MySQLModule, HttpServerModule) with Application class.
- Web routing configures the handler through the decorator.
- SQL normalization, avoiding heavy ORM, while also making readability.


Getting started
===============

Server
------

An example using a server:

.. code-block:: python

    # hello_handler.py

    from aiohttp import web
    from tomato.transport.http import Routes


    routes = Routes()

    @routes.get('/hello')
    @routes.get('/hello/{name}')
    async def xxx(request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)


.. code-block:: python

    # hello.py

    from hello_handler import routes
    from tomato.util import Application
    from tomato.transport import HttpServerModule


    app = Application()
    app['http_server'] = HttpServerModule(host='localhost', port=1024, routes_list=[routes, ])
    # app.run()
    # app.stop()
    app.run_forever()


MySQL
-----

.. code-block:: python

    import logging
    from tomato.util import Application
    from tomato.store import MySQLModule
    from tomato.store import SqlClauseAssemble
    from tomato.store import SqlParamCollections


    app = Application()
    # setting parameter is a dictionary type
    app['mysql'] = MySQLModule(setting=mysql_setting)
    app.run()
    sql_assemble = SqlClauseAssemble()
    sql_assemble.wanted_words = ['platform_id', 'open_id']
    sql_assemble.table_name = '`app_account_users`'
    where_params = SqlParamCollections()
    where_params.add_normal_param(('open_id', '=', 18888888888, True))
    sql_assemble.where_params = where_params
    (sql, params) = sql_assemble.get_query_clause()
    logging.info((sql, params))
    result_list = loop.run_until_complete(app['mysql'].get_all(sql,params))
    logging.info(result_list)
    app.stop()


Example
-------
please refer to `examples <https://github.com/tangmi001/tomatolib/tree/master/examples>`_.


Dependent library
=================

- `aiohttp <https://github.com/aio-libs/aiohttp>`_


Other contributors
==================
- zhouqinmin: zqm175899960@163.com
