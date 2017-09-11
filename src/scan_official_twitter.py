#!/usr/bin/python
"""
this script gets the top 40 coins of bittrex and then calls twitter accounts every couple of minutes with these coins
to find if they have posted anything of relevance.
"""

# TODO: how do we can and make meaning of well known exchanges?


def scan():
    # get coins from bittrex
    # sort volume
    # only top 40
    # ^^ put into shared function from rex.py
    # get all data from coin-info db
    # check if coin-info exists
    # if exists and has a twitter account
    # send twitter search
    # - check for tweets in the last 12 minutes
    # - if profile has something from last 12 minutes
    # - check if tweet has specific criteria (how do we define?)
    # else private message azurikai
