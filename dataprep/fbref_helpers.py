#!/usr/bin/env python

from web_helpers import *
from utils.converter import *
 
def decode_fixtures (web_content, matchweek):

    table_content = get_div (web_content, div_type = 'table', div_id = 'sched_2022-2023_208_1')
    # table_body = get_div (table_content, div_type = 'tbody')
    rows = get_fixture_rows (table_content, matchweek)

    matches = []
    for row in rows:
        matches.append (get_match_from_fixture_row(row))

    return matches
        
def get_match_from_fixture_row (row):
    cols = row.split ("</td>")
    home = scrape_info ( text = [col for col in cols if 'home_team' in col][0],
                         key = 'home_team',
                         left = 'Stats">', right = "<")
    away = scrape_info ( text = [col for col in cols if 'away_team' in col][0],
                         key = 'away_team',
                         left = 'Stats">', right = "<")
    score = scrape_info ( text = [col for col in cols if 'score' in col][0],
                         key = 'score',
                         left = 'Serie-A">', right = "<").replace ('&ndash;','-')
    
    
    return { 'home' : teamname2label(home), 'away' : teamname2label(away), 'goal_home' : score.split('-')[0], 'goal_away' : score.split('-')[-1] }

    
def get_fixture_rows (content, matchweek):
    return [x for x in content.split ('</tr>') if '"gameweek" >%s<' % matchweek in x]


def get_team_rows (content):
    return [x for x in content.split ('</tr>') if "team" in x]

def decode_perf (web_content):
    table_content = get_div (web_content, div_type = 'table',
                             div_id = 'stats_squads_standard_for',
                             extra_label = '<caption>Squad Standard Stats')
    perf = []

    rows = get_team_rows (table_content)
    for row in rows[1:]: # first row is header
        perf.append (get_perf (row))

    return perf

def get_perf (row):
    cols = row.split ("</td>")

    perf = {}
    perf['team'] = teamname2label ( scrape_info ( text = [col for col in cols if 'team' in col][0],
                                          key = 'team',
                                          left = 'Stats">', right = '<'  ) )

    features = ['goals_per90', 'assists_per90', 'goals_assists_per90',
                'goals_pens_per90', 'goals_assists_pens_per90']

    for feat in features:
        perf [feat] = scrape_info ( text = [col for col in cols if feat in col][0],
                                    key = feat,
                                    left = '"%s" >' % feat, right = '<' )

    return perf
