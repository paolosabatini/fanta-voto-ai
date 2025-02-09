#!/usr/bin/env python

"""
 FBREF helpers function for interpreting the content
 - decoding the fixtures from the dedicated page
 - decoding the performance from the standard stats page
"""

from dataprep.web_helpers import *
from utils.converter import *
from utils.globalvalues import is_regular_season

"""
 Get match report url for a team and a match day
"""
def get_matchreport_url_for_team_and_matchday(web_content, team_name, matchweek):
    
    is_this_match_in_regular_season = is_regular_season (matchweek)
    matchweek = format_matchweek (matchweek)
    
    table_content = get_div (web_content, div_type = 'table', div_id = 'sched_2023-2024_208_1')
    rows = [row for row in get_fixture_rows (table_content, matchweek) if team_name in row]
    # this is the case of "rest weeks" in the poule stage
    if (not is_this_match_in_regular_season and len(rows) == 1):
        return None
    return get_match_report_url_from_row ( rows[0] if is_this_match_in_regular_season else rows[-1])


"""
 Get the player stats for a whole team for a singlt match day from the matchreport
"""
def get_player_stats_for_team_from_matchreport  (web_content, team_name, matchweek):
    players = {}

    team_id = get_team_id_from_match_report (web_content, team_name)
    if not team_id:
        return players
    
    summary_content = get_div (web_content, div_type = 'table', div_id = 'stats_%s_summary' % team_id, extra_label = 'Player Stats Table')
    players_summary = get_summary_player_stats_from_match_report_table (summary_content)

    passing_content = get_div (web_content, div_type = 'table', div_id = 'stats_%s_passing' % team_id, extra_label = 'passes_progressive_distance') # put a stats that is only in this table
    players_passing = get_passing_player_stats_from_match_report_table (passing_content)

    defensive_content = get_div (web_content, div_type = 'table', div_id = 'stats_%s_defense' % team_id, extra_label = 'tackles_def_3rd') # put a stats that is only in this table
    defensive_passing = get_defensive_player_stats_from_match_report_table (defensive_content)

    possession_content = get_div (web_content, div_type = 'table', div_id = 'stats_%s_possession' % team_id, extra_label = 'tackles_def_3rd') # put a stats that is only in this table
    possession_passing = get_possession_player_stats_from_match_report_table (possession_content)

    
    exit()

    return players


"""
 Get the fixtures from the dedicated table given the matchweek
"""
def decode_fixtures (web_content, matchweek):

    table_content = get_div (web_content, div_type = 'table', div_id = 'sched_2023-2024_208_1')
    # table_body = get_div (table_content, div_type = 'tbody')
    rows = get_fixture_rows (table_content, matchweek)

    matches = []
    for row in rows:
        matches.append (get_match_from_fixture_row(row))

    return matches

"""
 Get summary player stats from match report
"""
def get_summary_player_stats_from_match_report_table (web_content):
    rows = get_player_rows(web_content)
    header_row = rows[0]
    players_rows = rows[1:-1]
    dict_these_players = {}
    for player_row in players_rows:
        name =  scrape_info (text = player_row,
                             key = 'player',
                             left = '<th', right = '</th>').split("</a>")[-2].split(">")[-1]
        if name == '': continue

        name = name2noutf8 (name)
        dict_these_players [name] = {}

        perf = {}
        features = ['shirtnumber', 'position', 'minutes', 'goals', 'assists', 'pens_made',
                    'pens_att', 'shots', 'shots_on_target', 'cards_yellow', 'cards_red', 'touches',
                    'tackles', 'interceptions', 'blocks', 'xg', 'npxg', 'xg_assist', 'sca',
                    'gca', 'passes_completed', 'passes', 'passes_pct', 'progressive_passes',
                    'carries', 'progressive_carries', 'take_ons', 'take_ons_won']
        
        for feat in features:
            perf [feat] = scrape_info ( text = player_row,
                                        key = feat,
                                        left = '"%s" >' % feat, right = '<' )
        dict_these_players [name] = perf

"""
 Get passing player stats from match report
"""
def get_passing_player_stats_from_match_report_table (web_content):
    rows = get_player_rows(web_content)
    header_row = rows[0]
    players_rows = rows[1:-1]
    dict_these_players = {}
    for player_row in players_rows:
        
        name =  scrape_info (text = player_row,
                             key = 'player',
                             left = '<th', right = '</th>').split("</a>")[-2].split(">")[-1]
        if name == '': continue
        
        name = name2noutf8 (name)
        dict_these_players [name] = {}



        perf = {}
        features = ['passes_completed', 'passes', 'passes_pct', 'passes_total_distance',
                    'passes_progressive_distance', 'passes_completed_short', 'passes_short',
                    'passes_pct_short', 'passes_completed_medium', 'passes_medium', 'passes_pct_medium',
                    'passes_completed_long', 'passes_long', 'passes_pct_long', 'assists',
                    'xg_assist', 'pass_xa', 'assisted_shots', 'passes_into_final_third',
                    'passes_into_penalty_area', 'crosses_into_penalty_area', 'progressive_passes'
                    ]
        
        for feat in features:
            try:
                perf [feat] = scrape_info ( text = player_row,
                                            key = feat,
                                            left = '"%s" >' % feat, right = '<' )
            except:
                print ("error feat %s player %s" % (feat,name))
        dict_these_players [name] = perf

    return dict_these_players

"""
 Get defensive player stats from match report
"""
def get_defensive_player_stats_from_match_report_table (web_content):
    rows = get_player_rows(web_content)
    header_row = rows[0]
    players_rows = rows[1:-1]
    dict_these_players = {}
    for player_row in players_rows:
        
        name =  scrape_info (text = player_row,
                             key = 'player',
                             left = '<th', right = '</th>').split("</a>")[-2].split(">")[-1]
        if name == '': continue
        
        name = name2noutf8 (name)
        dict_these_players [name] = {}



        perf = {}
        features = ['tackles', 'tackles_won', 'tackles_def_3rd', 'tackles_att_3rd', 'tackles_mid_3rd',
                    'challenge_tackles', 'challenge_tackles_pct', 'challenges_lost', 'blocked_passes',
                    'interceptions', 'tackles_interceptions', 'clearances', 'errors']
        
        for feat in features:
            try:
                perf [feat] = scrape_info ( text = player_row,
                                            key = feat,
                                            left = '"%s" >' % feat, right = '<' )
            except:
                print ("error feat %s player %s" % (feat,name))
        dict_these_players [name] = perf
        print (name, perf)

    return dict_these_players

"""
 Get team id from matchreport page (to ease the navigation)
"""
def get_team_id_from_match_report (web_content, team_name):
    list_of_club_logos = [img for img in get_list_of_images (web_content) if team_name in img and "Club Crest" in img and not "table" in img]
    try:
        source = [ value for value in list_of_club_logos[0].split(" ") if "src=" in value][0]
        
        return source.split(".png")[0].split("/")[-1]
    except:
        return None
    
"""
 Given the table row for fixtures, it provides the fixture
"""
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

"""
 Given the table row, get the match report url
"""
def get_match_report_url_from_row (row):
    return "https://fbref.com" + scrape_info (
        text = [col for col in row.split ("</td>") if 'match_report' in col][0],
        key = 'match_report',
        left = '<a href="', right = '">'
    )

"""
 Helper function for deconding the fixture rows
"""
def get_fixture_rows (content, matchweek):
    return [x for x in content.split ('</tr>') if '"gameweek" >%s<' % matchweek in x]

"""
 Helper function for deconding the player rows
"""
def get_player_rows (content):
    return [x for x in content.split ('</tr>') if "player" in x]

"""
 Helper function for deconding the team rows
"""
def get_team_rows (content):
    return [x for x in content.split ('</tr>') if "team" in x]

"""
 Given the table content, it gives the performance stats for the team
"""
def decode_perf (web_content):
    table_content = get_div (web_content, div_type = 'table',
                             div_id = 'stats_squads_standard_for',
                             extra_label = '<caption>Squad Standard Stats')
    perf = []

    rows = get_team_rows (table_content)
    for row in rows[1:]: # first row is header
        perf.append (get_perf (row))

    return perf

"""
 Decoding the team performance from the row content
"""
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
