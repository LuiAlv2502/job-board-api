"""
Database layer - plain psycopg2, no ORM.
"""
import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from psycopg2 import pool
from psycopg2 import OperationalError

# Configuramos variables de entorno individuales con valores por defecto
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123")
DB_NAME = os.environ.get("DB_NAME", "jobboard")
DB_PORT = os.environ.get("DB_PORT", "5433")

connection_pool = None


def _get_pool() -> pool.SimpleConnectionPool:
    global connection_pool
    if connection_pool is None:
        try:
            # Creamos un diccionario con los parámetros individuales que deseas usar
            db_config = {
                "host": DB_HOST,
                "user": DB_USER,
                "password": DB_PASSWORD,
                "database": DB_NAME,
                "port": DB_PORT
            }
            
            # Pasamos los parámetros usando ** para desempaquetar el diccionario
            connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                **db_config
            )
        except OperationalError as exc:
            raise RuntimeError(
                "Could not connect to PostgreSQL. Verify your credentials in DB_HOST, DB_USER, etc., "
                f"or check your Docker container. Attempted connecting to {DB_USER}@{DB_HOST}/{DB_NAME}"
            ) from exc
    return connection_pool


@contextmanager
def get_conn():
    conn = _get_pool().getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _get_pool().putconn(conn)


@contextmanager
def get_cursor():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield cur
        finally:
            cur.close()


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS applicants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    description TEXT,
    location VARCHAR(150),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    applicant_id INTEGER NOT NULL REFERENCES applicants(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL DEFAULT 'submitted',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (applicant_id, job_id)
);

CREATE INDEX IF NOT EXISTS idx_applications_applicant_id ON applications(applicant_id);
CREATE INDEX IF NOT EXISTS idx_applications_job_id ON applications(job_id);
"""


def init_db() -> None:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(SCHEMA_SQL)
        cur.close()