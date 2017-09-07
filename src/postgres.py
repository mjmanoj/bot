import os
import psycopg2
import urlparse
from config import env


class Db():
    """ contextual database for setting up and tearing down before running functional methods."""
    # intilize

    def __init__(self, url=urlparse.urlparse(os.environ["DATABASE_URL"])):
        urlparse.uses_netloc.append("postgres")
        self.url = url
        self.conn = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )
        self.cur = self.conn.cur()

    # setup
    def __enter__(self):
        return self.cur

    # teardown
    def __exit__(self, *args):
        self.cur.close()
        self.conn.close()


def add_coin_symbol(entry):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    with Db() as db:
        table = env + "/scores"
        created, score = entry
        db.execute("insert into " + table +
                   "(created, score) values (%s, %s, %s)", (created, score))


def add_operations_log(log):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    with Db() as db:
        table = env + "/moon_call"
        init, end, twitter_search_start, twitter_search_end, track_periphreals_start, track_periphreals_end, send_message_start, send_message_end = log
        db.execute("insert into " + table +
                   "(init, end, twitter_search_start, twitter_search_end, send_message_start, send_message_end) values (%s, %s, %s, %s, %s, %s)",
                   (init, end, twitter_search_start, twitter_search_end, send_message_start, send_message_end))


def get_historical_scores(cutoff):
    with Db() as db:
        table = env + "/scores"
        db.execute("select * from " + table +
                   " where created >= " + cutoff + "")
        return db.fetchall()


def get_moon_call_operations(cutoff):
    with Db() as db:
        table = env + "/moon_call"
        db.execute("SELECT * from " + table + " order by init desc limit 1")
        return db.fetchall()
