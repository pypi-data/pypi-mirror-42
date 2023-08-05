import logging
import select
import threading
from contextlib import contextmanager
from textwrap import dedent

from huey.api import Huey
from huey.constants import EmptyData
from huey.storage import BaseStorage
from psycopg2.extensions import (
    ISOLATION_LEVEL_AUTOCOMMIT,
    quote_ident,
)


logger = logging.getLogger(__name__)


@contextmanager
def transaction(pool):
    # Manage the connection, transaction and cursor from a connection pool.
    conn = pool.getconn()
    try:
        with conn:  # Wraps in a transaction.
            with conn.cursor() as curs:
                yield curs
    finally:
        pool.putconn(conn)


class PostgresHuey(Huey):
    def get_storage(self, *, connection_pool):
        return PostgresStorage(huey=self, connection_pool=connection_pool)


class PostgresStorage(BaseStorage):
    def __init__(self, *, name='huey', huey, connection_pool):
        super(PostgresStorage, self).__init__(name=name)
        self.pool = connection_pool
        self.huey = huey
        self._local = threading.local()

    @property
    def listen_connection(self):
        if not hasattr(self._local, 'listen_connection'):
            logger.info("New pg connection.")
            self._local.listen_connection = conn = self.pool.getconn()
            # This is for NOTIFY consistency, according to psycopg2 doc.
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            channel = quote_ident(f"huey.{self.name}.enqueue", conn)
            with conn.cursor() as curs:
                logger.debug("Listening on channel %s.", channel)
                curs.execute(f"LISTEN {channel};")
        return self._local.listen_connection

    @property
    def notifies(self):
        if not hasattr(self._local, 'notifies'):
            self._local.notifies = []
        return self._local.notifies

    def consume_one(self, mid):
        # Race to process this message.
        with transaction(self.pool) as curs:
            curs.execute(dedent("""\
            UPDATE huey.queue
            SET "state" = 'consumed'
            WHERE id = %s AND "state" = 'queued'
            RETURNING message;
            """), (mid,))
            # If no row was updated, this mean another worker has consumed it.
            if 1 == curs.rowcount:
                message, = curs.fetchone()
                return message

    def dequeue(self):
        while True:
            # Start by processing already fetched notifies.
            while self.notifies:
                notify = self.notifies.pop(0)
                mid = int(notify.payload)
                message = self.consume_one(mid)
                if message:
                    logger.info("Consumed message %s.", mid)
                    return message
                else:
                    logger.info("Message %s already consumed.", mid)

            # Notify list is empty, listen for more. (blocking)
            self.listen()

    def enqueue(self, data):
        insert = (dedent("""\
        INSERT INTO huey.queue("state", message)
        VALUES (%s, %s)
        RETURNING id;
        """), ("queued", data))

        with transaction(self.pool) as curs:
            curs.execute(*insert)
            id_, = curs.fetchone()
            channel = quote_ident(f"huey.{self.name}.enqueue", curs)
            curs.execute(f"""NOTIFY {channel}, %s;""", (str(id_),))

    def listen(self):
        with self.listen_connection.cursor() as curs:
            while not self.notifies:
                fd_lists = select.select([curs.connection], [], [], 300)
                if any(fd_lists):
                    curs.connection.poll()
                    self._local.notifies += curs.connection.notifies
                    logger.info("Got %s.", curs.connection.notifies)
                    curs.connection.notifies[:] = []

    def peek_data(self, key):
        return EmptyData

    def read_schedule(self, *_):
        return []
