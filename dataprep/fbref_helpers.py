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



