import os
import psycopg2
import urlparse
from config import env

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def add_coin_symbol(entry):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cur()
    table = env + "/scores
    created, score = entry
    cur.execute("insert into " + table +
                "(created, score) values (%s, %s, %s)", (created, score))
    cur.close()
    conn.close()


def add_operations_log(log):
    """ adds a coin symbol to the symbols table according to environment, and the symbol it is."""
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cur()
    table = env + "/moon_call"
    init, end, twitter_search_start, twitter_search_end, track_periphreals_start, track_periphreals_end, send_message_start, send_message_end = log
    cur.execute("insert into " + table +
                "(init, end, twitter_search_start, twitter_search_end, send_message_start, send_message_end) values (%s, %s, %s, %s, %s, %s)",
                (init, end, twitter_search_start, twitter_search_end, send_message_start, send_message_end))
    cur.close()
    conn.close()


def get_historical_scores(cutoff):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cur()
    table = env + "/scores"
    cur.execute("select * from " + table + " where created >= " + cutoff + "")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_moon_call_operations(cutoff):
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cur()
    table = env + "/scores"
    cur.execute("SELECT * from " + table + " order by init desc limit 1"))
    rows=cur.fetchall()
    cur.close()
    conn.close()
    return rows
