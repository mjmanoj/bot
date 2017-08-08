"""
db is a tinydb adapter with useful function calls
"""
from tinydb import TinyDB, Query
import os
cwd = os.getcwd()


# finds an object by id in a tindydb database
def find_by_id(location, id):
    query = Query()
    database = get_database(location)
    return database.search(query.id == id)


# adds an object to a database
def add(location, x):
    database = get_database(location)
    database.insert(x)


# get_database gets a database
def get_database(x):
    path = cwd + "/db/" + x + ".json"
    return TinyDB(path)
