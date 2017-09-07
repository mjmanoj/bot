#!/usr/bin/python
""" the db package is a tinydb adapter with useful function calls """
import os
from tinydb import TinyDB, Query
from helpers import mkdir_p, touch
from config import env
CWD = os.getcwd()


# finds an object by id in a tindydb database
def find_by_id(path, file_name, identifier):
    """ find_by_id finds an item by an identifier in its respective database """

    query = Query()
    database = get_database(path="", file_name=file_name)
    return database.search(query.id == identifier)


# adds an object to a database
def add(path, file_name, entry):
    """ add inserts an entry into its respective database """

    database = get_database(path, file_name)
    database.insert(entry)


# get_database gets a database
def get_database(path, file_name):
    """
    get_database is a helper function that gets the proper database based on
    path and file_name location
    """

    directory = CWD + "/db/" + env + "/" + path
    db = directory + "/" + file_name + ".json"

    if not os.path.isdir(directory):
        mkdir_p(directory)
    if not os.path.exists(db):
        touch(db)

    return TinyDB(db)


def get(path, file_name):
    """ get returns all entries from the respective database """

    database = get_database(path, file_name)
    all_entries = database.all()
    return all_entries
