import os
import psycopg2
import psycopg2.extras
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
        self.cur = self.conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    # setup
    def __enter__(self):
        return self

    # teardown
    def __exit__(self, *args):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


def add_twitter_score(entry):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    with Db() as db:
        table = str(env + "_twitter_scores")
        try:
            db.cur.execute("insert into " + table +
                           "(symbol, score, exchange) values (%s, %s, %s)", (entry["symbol"], entry["score"], "bittrex"))
        except psycopg2.Error as e:
            print e
            pass


def add_operations_log(log):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    with Db() as db:
        table = str(env + "_moon_call")
        try:
            db.cur.execute("insert into " + table +
                           "(main_start, main_end, twitter_search_start, twitter_search_end, send_message_start, send_message_end, daily_coins, weekly_coins) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (log["main_start"], log["main_end"], log["twitter_search_start"], log["twitter_search_end"], log["send_message_start"], log["send_message_end"], log["daily_coins"], log["weekly_coins"]))
        except psycopg2.Error as e:
            print e
            pass


def add_twitter_call_log(log):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    with Db() as db:
        table = str(env + "_twitter_call")
        try:
            db.cur.execute("insert into " + table +
                           "(start, end, duration) values (%s, %s, %s)",
                           (log["start"], log["end"], log["duration"]))
        except psycopg2.Error as e:
            print e
            pass


def add_calendar_event(symbol, date, link):
    """ adds a calendar event to the calendar table according to environment."""
    with Db() as db:
        table = str(env + "_calendar_events")
        try:
            db.cur.execute("insert into " + table +
                           "(symbol, date, link) values (%s, %s, %s)",
                           (symbol, date, link))
        except psycopg2.Error as e:
            print e
            pass


def get_historical_twitter_scores(cutoff):
    with Db() as db:
        table = str(env + "_twitter_scores")
        try:
            db.cur.execute("select * from " + table +
                           " where created >= '" + str(cutoff) + "' order by score desc")
        except psycopg2.Error as e:
            print e
            return []

        return db.cur.fetchall()


def get_coin_infos(cutoff):
    with Db() as db:
        table = str(env + "_coin_info")
        try:
            db.cur.execute("select * from " + table +
                           " where created >= '" + str(cutoff))
        except psycopg2.Error as e:
            print e
            return []

        return db.cur.fetchall()


def get_moon_call_operations():
    with Db() as db:
        table = str(env + "_moon_call")
        try:
            db.cur.execute("SELECT * from " + table +
                           " order by main_start desc limit 1")
        except psycopg2.Error as e:
            print e
            pass
        return db.cur.fetchone()


def get_last_twitter_scan_duration():
    with Db() as db:
        table = str(env + "_twitter_call")
        try:
            db.cur.execute("SELECT * from " + table +
                           " order by start desc limit 1")
        except psycopg2.Error as e:
            print e
            pass
        return db.cur.fetchone()
