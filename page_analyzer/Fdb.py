from psycopg2.extras import RealDictCursor
from psycopg2.errorcodes import UNIQUE_VIOLATION
import psycopg2
from psycopg2 import errors
from datetime import datetime


class FDataBase:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.dbname)

    def closed(self):
        self.conn.close()
        self.conn = None

    def add_url(self, named: str):
        """  Add id, url in db.url  """
        now = datetime.now()
        try:
            self.connect()
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""INSERT INTO urls (name, created_at)
                 VALUES (%s, %s) RETURNING id;""", (named, now))
                self.conn.commit()
                return curs.fetchone()["id"]
        except errors.lookup(UNIQUE_VIOLATION):
            return 'nouniq'

    def add_urls(self, url_id: id, status_code: id, h1: str, title: str,
                 description: str):
        """ Add seo in db.url_checks """
        now = datetime.now()
        try:
            self.connect()
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("""INSERT INTO url_checks (url_id, status_code, h1,
                 title, description, created_at) VALUES (%s, %s, %s, %s, %s,
                  %s); """, (url_id, status_code, h1, title, description, now))
                self.conn.commit()
        finally:
            self.closed()

    def get_name(self, name: str) -> dict:
        """ Check and returns name from db.urls """
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                name_ = [name, ]
                curs.execute("SELECT * FROM urls WHERE name = ANY(%s);",
                             (name_,))
                return curs.fetchone()
        finally:
            self.closed()

    def get_id(self, id):
        """ Returns name url and date from db.urls """
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                id_ = [id, ]
                curs.execute("SELECT * FROM urls WHERE id = ANY(%s);", (id_,))
                return curs.fetchone()
        finally:
            self.closed()

    def get_for_urls(self):
        """ Returns name id, url, data check, name,
            status_code from db.url and db.urls """
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute("select u.id, name, uc.created_at, status_code"
                             " from urls as u left join "
                             "(SELECT url_id, max(id) as maxid FROM url_checks "
                             "GROUP BY url_checks.url_id) as t "
                             "on u.id = t.url_id left join url_checks as uc "
                             "on uc.id = t.maxid order by u.id DESC;", )
                return curs.fetchall()
        finally:
            self.closed()

    def get_for_url_checks(self, url_id):
        """ Returns seo in db.url_checks """
        self.connect()
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
                id_ = [url_id, ]
                curs.execute("SELECT * FROM url_checks WHERE url_id = ANY(%s) "
                             "ORDER BY created_at DESC;", (id_,))
                return curs.fetchall()
        finally:
            self.closed()
