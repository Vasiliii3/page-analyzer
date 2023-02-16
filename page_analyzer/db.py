import os
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2.extras import RealDictCursor

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
file = os.path.join(Path(__file__).parent.parent, 'database.sql')


def create_db():
    """Auxiliary function for creating database tables"""
    conn = connect()
    cursor = conn.cursor()
    with open(file, mode='r') as db_file:
        cursor.execute(db_file.read())
    conn.commit()
    conn.close()


def connect():
    return psycopg2.connect(DATABASE_URL)


def add_url(named: str):
    """  Add id, url in db.url  """
    now = datetime.now()
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("""INSERT INTO urls (name, created_at)
             VALUES (%s, %s) RETURNING id;""", (named, now))
            conn.commit()
            return curs.fetchone()["id"]
    except errors.lookup(UNIQUE_VIOLATION):
        return 'nouniq'
    finally:
        conn.close()


def add_urls(url_id: id, status_code: id, h1: str, title: str,
             description: str):
    """ Add seo in db.url_checks """
    now = datetime.now()
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("""INSERT INTO url_checks (url_id, status_code, h1,
             title, description, created_at) VALUES (%s, %s, %s, %s, %s,
              %s); """, (url_id, status_code, h1, title, description, now))
            conn.commit()
    finally:
        conn.close()


def get_name(name: str) -> dict:
    """ Check and returns name from db.urls """
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            name_ = [name, ]
            curs.execute("SELECT * FROM urls WHERE name = ANY(%s);",
                         (name_,))
            return curs.fetchone()
    finally:
        conn.close()


def get_id(id):
    """ Returns name url and date from db.urls """
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            id_ = [id, ]
            curs.execute("SELECT * FROM urls WHERE id = ANY(%s);", (id_,))
            return curs.fetchone()
    finally:
        conn.close()


def get_for_urls():
    """ Returns name id, url, data check, name,
        status_code from db.url and db.urls """
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("select u.id, name, uc.created_at, status_code"
                         " from urls as u left join "
                         "(SELECT url_id, max(id) as maxid FROM url_checks "
                         "GROUP BY url_checks.url_id) as t "
                         "on u.id = t.url_id left join url_checks as uc "
                         "on uc.id = t.maxid order by u.id DESC;", )
            return curs.fetchall()
    finally:
        conn.close()


def get_for_url_checks(url_id):
    """ Returns seo in db.url_checks """
    conn = connect()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            id_ = [url_id, ]
            curs.execute("SELECT * FROM url_checks WHERE url_id = ANY(%s) "
                         "ORDER BY created_at DESC;", (id_,))
            return curs.fetchall()
    finally:
        conn.close()
