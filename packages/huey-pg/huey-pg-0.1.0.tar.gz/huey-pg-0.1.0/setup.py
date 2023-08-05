# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['huey_pg']
install_requires = \
['huey>=1.11,<2.0', 'psycopg2>=2.7,<3.0']

setup_kwargs = {
    'name': 'huey-pg',
    'version': '0.1.0',
    'description': 'Postgres Broker for Huey Task Queue',
    'long_description': '=====================================\n huey-pg -- Postgres Broker for Huey\n=====================================\n\nhuey_ is a simple task queue implementation for Python. huey-pg provides a\nPostgres-based implementation of a huey storage.\n\n**The project is not feature complete yet.**\n\n\nFeatures\n========\n\n- Super simple deployment.\n- Stores messages in a single table.\n- All data are wrapped in a dedicated schema.\n- Uses LISTEN/NOTIFY to keep worker sync. No polling.\n- Reliable thanks to Postgres MVCC.\n- Using plain psycopg2. No ORM.\n\n\nInstallation\n============\n\n- Install huey-pg package from PyPI::\n\n      pip install huey-pg\n\n- Apply ``huey-pg.sql`` file in your database::\n\n      psql -f huey-pg.sql\n\n- Then use ``PostgresHuey`` class:\n\n      import psycopg2.pool\n      from huey_pg import PostgresHuey\n\n      pool = psycopg2.pool.ThreadedConnectionPool(0, 4, conninfo)\n      huey = Postgres(connection_pool=pool))\n\n      @huey.task\n      def hello(name):\n          print(f"Hello {name}!")\n\nRoadmap\n=======\n\n- Process missed notifies while resuming worker.\n- Functionnal tests.\n- Result storage.\n- Delayed & scheduled task.\n\n\n.. _huey:: https://huey.rtfd.io/\n',
    'author': 'Étienne BERSAC',
    'author_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
