"""
the db package is a tinydb adapter with useful function calls
"""
from tinydb import TinyDB, Query
from helpers import mkdir_p, touch
import os
from config import env
cwd = os.getcwd()


# finds an object by id in a tindydb database
def find_by_id(path, file_name, identifier):
    query = Query()
    database = get_database(path="", file_name=file_name)
    return database.search(query.id == identifier)


# adds an object to a database
def add(path, file_name, entry):
    database = get_database(path, file_name)
    database.insert(entry)


# get_database gets a database
def get_database(path, file_name):
    directory = cwd + "/db/" + env + "/" + path
    db = directory + "/" + file_name + ".json"

    if not os.path.isdir(directory):
        mkdir_p(directory)
    if not os.path.exists(db):
        touch(db)

    return TinyDB(db)


def get(path, file_name):
    database = get_database(path, file_name)
    all_entries = database.all()
    return all_entries
