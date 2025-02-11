#!/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
import utils.db.DbPlayers as dbp

_is_instanced = False
_players = []

def is_instanced():
    return _is_instanced

def get_all_players():
    instance()
    return _players

def retrieve_all_players():

    _players = dbp.DbPlayers().get_all_players()
    # logging.info ("Initialized Player List:\t%d" % len(_players))
    return _players

def instance():
    if not is_instanced():
        retrieve_all_players()
        _is_instanced = True 
 
