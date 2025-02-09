#!/usr/bin/env python
# coding=utf8   

"""
 FIGC interpreter helping function
 - get the list of teams from the main page
 - get the list and stats of player from team page
 - get the list of players from the team page
"""

# get the list of team from the home page of clubs
def get_dict_of_teams (content, base_url=''):
    dict_of_teams = {}
    main_content = content.split ("<!-- MAIN-->")[1]
    list_of_team_source = [ x.strip() for x in main_content.splitlines() if 'data-udi' in x]
    # list_of_team_source = [x for x in main_content.splitlines()] # if 'data-udi' in x]
    for team_source in list_of_team_source:
        
        name = ( [ x for x in team_source.split (" ") if 'title=' in x][0].replace('title=','').strip('"') )
        url = [ x for x in team_source.split (" ") if 'data-udi=' in x][0].replace('data-udi=','').strip('"').split ('/')[-2]
        dict_of_teams [ name ] = base_url+url
        
    return dict_of_teams

# get the stats of each player given the page content of a club
def decode_these_players (content, team_name):
    from utils.converter import teamname2label, name2noutf8
    from dataprep.web_helpers import scrape_info
    list_of_player_texts = [ x.replace ('</tr>','') for x in content.split ('<tr>') if '</tr>' in x]
    dict_these_players = {}
    
    for player_text in list_of_player_texts:
        name =  scrape_info (text = player_text,
                             key = 'Giocatore',
                             left = 'playerUuid=', right = '</a>').split('>')[-1]
        
        if name == '': continue

        name = name2noutf8 (name)
        dict_these_players [name] = {}
        
        dict_these_players [name] ['Maglia'] = scrape_info (text = player_text,
                                                            key = 'Maglia',
                                                            left = '<span>', right='</span>')
        
        features = ['Ruolo', 'Presenze', 'Goal', 'Cartellini gialli', 'Cartellini rossi',
                    'Minuti giocati', 'Presenze da titolare', 'Presenze da titolare',
                    'Falli commessi', 'Falli subiti', 'Fuorigioco', 'Tiri',
                    'Tiri in porta', 'Autogoal']
        
        for feature in features:
            dict_these_players [name] [feature.replace (' ','_')] = scrape_info (text = player_text,
                                                                                 key = feature,
                                                                                 left = 'data-title="%s">' % feature,
                                                                                 right='</td>')
        
        dict_these_players [name] ['Squadra'] =  teamname2label (team_name)
        
    return dict_these_players

