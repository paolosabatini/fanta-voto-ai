#!/usr/bAin/env python3
import logging
logger = logging.getLogger(__name__)

import utils.singleton.PlayerListSingleton as pls
from unidecode import unidecode
import re

'''
Helper functions
'''
_characters="-"
def get_stat_from_row ( row, data_stat, is_name = False):
    base_field = row.find("th" if is_name else "td", attrs={"data-stat":data_stat})
    return base_field.a.contents[0] if is_name else base_field.contents[0]

def prepare_name (name):
    return unidecode (re.sub (_characters, ' ', name.replace("  "," ")))

def match_names(csv_name, reference_name):
    csv_name_prepared = prepare_name(csv_name)
    reference_name_prepared = prepare_name(reference_name)

    name_and_surname_matching = (csv_name_prepared.strip() == reference_name_prepared.strip())
    only_surname_matching = (csv_name_prepared.split(" ")[-1] == reference_name_prepared.split(" ")[-1])
    is_composite_surname = ( " ".join( reference_name_prepared.split()[-2:] ) ==  " ".join( csv_name_prepared.split()[-2:]) )
    swapped_composite_surname = (reference_name_prepared.split()[-2] == csv_name_prepared.split()[-1] ) or (reference_name_prepared.split()[-1] == csv_name_prepared.split()[-2] )
    is_victoria_della = (reference_name_prepared == "Victoria Della") and csv_name_prepared == "Tori Dellaperuta"

    total_matching_condition = name_and_surname_matching \
        or only_surname_matching or is_composite_surname \
        or swapped_composite_surname or is_victoria_della

    return total_matching_condition

'''
TODO: Make it more configurable
'''
class PlayerStats:

    id = None
    team = None
    match_ref = None
    gk_stats_filled= False
    def __init__(self):
        self.name = str()
        self.pos = str()
        self.min = 0
        #general
        self.goal = 0
        self.assist = 0
        self.pen = 0
        self.pen_attempted = 0
        self.shots = 0
        self.shots_on_target = 0
        self.yellow_card = 0
        self.red_card = 0
        self.touches = 0
        self.tackles = 0
        self.intercepts = 0
        self.blocks = 0
        self.xg = 0
        self.npxg = 0
        self.xa = 0
        self.shot_creating_actions = 0
        self.goal_creating_actions = 0
        self.pass_completed = 0
        self.pass_attempted = 0
        self.progressive_pass = 0
        self.carries = 0
        self.progressive_carries = 0
        self.dribbles = 0
        self.dribbles_attempted = 0
        #events
        self.pen_failed = 0
        self.pen_scored = 0
        self.own_goals = 0
        
    def __init__ (self, row):
        self.name = get_stat_from_row( row = row, data_stat = "player", is_name=True)
        self.pos = get_stat_from_row(row, "position")
        self.min = get_stat_from_row(row, "minutes")
        self.goal= get_stat_from_row(row, "goals")
        self.assist = get_stat_from_row(row, "assists")
        self.pen = get_stat_from_row(row, "pens_made")
        self.pen_attempted = get_stat_from_row(row, "pens_att")
        self.shots = get_stat_from_row(row, "shots")
        self.shots_on_target = get_stat_from_row(row, "shots_on_target")
        self.yellow_card = get_stat_from_row(row, "cards_yellow")
        self.red_card = get_stat_from_row(row, "cards_red")
        self.touches = get_stat_from_row(row, "touches")
        self.tackles = get_stat_from_row(row, "tackles")
        self.intercepts = get_stat_from_row(row, "interceptions")
        self.blocks = get_stat_from_row(row, "blocks")
        self.xg = get_stat_from_row(row, "xg")
        self.npxg = get_stat_from_row(row, "npxg")
        self.xa = get_stat_from_row(row, "xg_assist")
        self.shot_creating_actions = get_stat_from_row(row, "sca")
        self.goal_creating_actions = get_stat_from_row(row, "gca")
        self.pass_completed = get_stat_from_row(row, "passes_completed")
        self.pass_attempted = get_stat_from_row(row, "passes")
        self.progressive_pass = get_stat_from_row(row, "progressive_passes")
        self.carries = get_stat_from_row(row, "carries")
        self.progressive_carries = get_stat_from_row(row, "progressive_carries")
        self.dribbles = get_stat_from_row(row, "take_ons_won")
        self.dribbles_attempted = get_stat_from_row(row, "take_ons")
        #events
        self.pen_failed = 0
        self.pen_scored = 0
        self.own_goals = 0

        
    def fill_gk_stats (self,row):
        self.gk_stats_filled = True
        self.gk_sota = get_stat_from_row(row, "gk_shots_on_target_against")
        self.gk_ga = get_stat_from_row(row, "gk_goals_against")
        self.gk_saves = get_stat_from_row(row, "gk_saves")
        self.gk_psxg = get_stat_from_row(row, "gk_psxg")
        self.gk_launches_completed = get_stat_from_row(row, "gk_passes_completed_launched")
        self.gk_launches = get_stat_from_row(row, "gk_passes_launched")
        self.gk_passes = get_stat_from_row(row, "gk_passes")
        self.gk_throws = get_stat_from_row(row, "gk_passes_throws")
        self.gk_avg_pass_length = get_stat_from_row(row, "gk_passes_length_avg")
        self.gk_crosses = get_stat_from_row(row, "gk_crosses")
        self.gk_crosses_stopped = get_stat_from_row(row, "gk_crosses_stopped")
        self.gk_def_actions_outside_box = get_stat_from_row(row, "gk_def_actions_outside_pen_area")
        # self.gk_avg_distance_def_actions = get_stat_from_row(row, "gk_avg_distance_def_actions")
        # events
        self.gk_pen_saved = 0
        
    def has_valid_gk_stats (self):
        all_gk_stats = ["gk_sota", "gk_ga", "gk_saves", "gk_psxg",
                        "gk_launches_completed", "gk_launches", "gk_passes",
                        "gk_throws", "gk_avg_pass_length", "gk_crosses",
                        "gk_crosses", "gk_crosses_stopped", "gk_def_actions_outside_box", "gk_pen_saved"]
        return self.gk_stats_filled \
            and all ( hasattr (self, stat) for stat in all_gk_stats)
    
        
    def find_id(self):
        all_players = pls.retrieve_all_players()
        name_matches = [ pl for pl in all_players if (match_names ( pl[-2].strip()+" "+pl[-1].strip(), self.name.strip()))]

        if len (name_matches) ==0:
            # Not found
            return False
        if len (name_matches)>1:
            # More than one match: using the exact match
            name_matches = [ pl for pl in all_players if ( ( pl[-2].strip()+" "+pl[-1].strip() == self.name.strip()))]
        try:
            self.id = int(name_matches[0][0])
            self.fanta_pos = str(name_matches[0][1])
        except:
            logging.error ("[ERROR] %s ID not found (n. matches = %d)" % (self.name, len(name_matches)))
            return False
        return True


    def set_mark(self, mark):
        self.mark = mark

    def set_match_ref (self, match_ref):
        self.match_ref = match_ref
