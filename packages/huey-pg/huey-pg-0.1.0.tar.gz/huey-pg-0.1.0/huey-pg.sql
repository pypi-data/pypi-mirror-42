\set ON_ERROR_STOP on

CREATE SCHEMA huey;

CREATE TYPE huey."state" AS ENUM (
  'queued',
  'consumed',
  'rejected',
  'done'
);

CREATE TABLE huey.queue(
  id SERIAL PRIMARY KEY,
  queue_name TEXT NOT NULL DEFAULT 'default',
  "state" huey."state",
  message bytea
);
