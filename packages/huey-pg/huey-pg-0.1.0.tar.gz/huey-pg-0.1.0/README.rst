=====================================
 huey-pg -- Postgres Broker for Huey
=====================================

huey_ is a simple task queue implementation for Python. huey-pg provides a
Postgres-based implementation of a huey storage.

**The project is not feature complete yet.**


Features
========

- Super simple deployment.
- Stores messages in a single table.
- All data are wrapped in a dedicated schema.
- Uses LISTEN/NOTIFY to keep worker sync. No polling.
- Reliable thanks to Postgres MVCC.
- Using plain psycopg2. No ORM.


Installation
============

- Install huey-pg package from PyPI::

      pip install huey-pg

- Apply ``huey-pg.sql`` file in your database::

      psql -f huey-pg.sql

- Then use ``PostgresHuey`` class:

      import psycopg2.pool
      from huey_pg import PostgresHuey

      pool = psycopg2.pool.ThreadedConnectionPool(0, 4, conninfo)
      huey = Postgres(connection_pool=pool))

      @huey.task
      def hello(name):
          print(f"Hello {name}!")

Roadmap
=======

- Process missed notifies while resuming worker.
- Functionnal tests.
- Result storage.
- Delayed & scheduled task.


.. _huey:: https://huey.rtfd.io/
