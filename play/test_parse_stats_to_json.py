#/usr/bin/env python3

import urllib.request
import re
from bs4 import BeautifulSoup
import csv, json
from unidecode import unidecode

_debug = False
_all_players = None
_characters = "-"
# _url = "https://fbref.com/en/matches/c2bd76dd/Lazio-FC-Como-Women-November-2-2024-Serie-A"
_url = "https://fbref.com/en/matches/38e744ff/Fiorentina-Sampdoria-September-22-2024-Serie-A"
_calciatrici = "./Calciatrici.csv"
_json_output = "./stats.json"

fp = urllib.request.urlopen(_url)
html = fp.read().decode("utf8")
parsed_html = BeautifulSoup (html,"html.parser")


# -----------------------------------------

def prepare_name (name):
    return unidecode (re.sub (_characters, ' ', name.replace("  "," ")))

def match_names ( csv_name, reference_name):
    csv_name_prepared = prepare_name(csv_name)
    reference_name_prepared = prepare_name(reference_name)

    name_and_surname_matching = (csv_name_prepared.strip() == reference_name_prepared.strip())
    only_surname_matching = (csv_name_prepared.split(" ")[-1] == reference_name_prepared.split(" ")[-1])
    is_composite_surname = ( " ".join( reference_name_prepared.split()[-2:] ) ==  " ".join( csv_name_prepared.split()[-2:]) )
    swapped_composite_surname = (reference_name_prepared.split()[-2] == csv_name_prepared.split()[-1] ) or (reference_name_prepared.split()[-1] == csv_name_prepared.split()[-2] )
    is_victoria_della = (reference_name_prepared == "Victoria Della") and csv_name_prepared == "Tori Dellaperuta"
    
    total_matching_condition = name_and_surname_matching or only_surname_matching or is_composite_surname or swapped_composite_surname or is_victoria_della
    if total_matching_condition and _debug:
        print ("MATCHING")
        print ("\tCSV: %s\t REF:%s" % (csv_name_prepared, reference_name_prepared))
        print ("\tname + surname matching = %s" % name_and_surname_matching)
        print ("\tonly surname matching = %s" % only_surname_matching)
        print ("\tfound composite = %s" % is_composite_surname)
        print ("\tswapped_composite_surnmae = %s" % swapped_composite_surname)
        print ("\tis_victoria_della = %s" % is_victoria_della)
        
    return total_matching_condition

# -----------------------------------------
class playerstat:
    id = None
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


    def __init__ (self, row):
        self.name = row.find("th", attrs={"data-stat":"player"}).a.contents[0]
        self.pos = row.find("td", attrs={"data-stat":"position"}).contents[0]
        self.min = row.find("td", attrs={"data-stat":"minutes"}).contents[0]
        self.goal= row.find("td", attrs={"data-stat":"goals"}).contents[0]
        self.assist = row.find("td", attrs={"data-stat":"assists"}).contents[0]
        self.pen = row.find("td", attrs={"data-stat":"pens_made"}).contents[0]
        self.pen_attempted = row.find("td", attrs={"data-stat":"pens_att"}).contents[0]
        self.shots = row.find("td", attrs={"data-stat":"shots"}).contents[0]
        self.shots_on_target = row.find("td", attrs={"data-stat":"shots_on_target"}).contents[0]
        self.yellow_card = row.find("td", attrs={"data-stat":"cards_yellow"}).contents[0]
        self.red_card = row.find("td", attrs={"data-stat":"cards_red"}).contents[0]
        self.touches = row.find("td", attrs={"data-stat":"touches"}).contents[0]
        self.tackles = row.find("td", attrs={"data-stat":"tackles"}).contents[0]
        self.intercepts = row.find("td", attrs={"data-stat":"interceptions"}).contents[0]
        self.blocks = row.find("td", attrs={"data-stat":"blocks"}).contents[0]
        self.xg = row.find("td", attrs={"data-stat":"xg"}).contents[0]
        self.npxg = row.find("td", attrs={"data-stat":"npxg"}).contents[0]
        self.xa = row.find("td", attrs={"data-stat":"xg_assist"}).contents[0]
        self.shot_creating_actions = row.find("td", attrs={"data-stat":"sca"}).contents[0]
        self.goal_creating_actions = row.find("td", attrs={"data-stat":"gca"}).contents[0]
        self.pass_completed = row.find("td", attrs={"data-stat":"passes_completed"}).contents[0]
        self.pass_attempted = row.find("td", attrs={"data-stat":"passes"}).contents[0]
        self.progressive_pass = row.find("td", attrs={"data-stat":"progressive_passes"}).contents[0]
        self.carries = row.find("td", attrs={"data-stat":"carries"}).contents[0]
        self.progressive_carries = row.find("td", attrs={"data-stat":"progressive_carries"}).contents[0]
        self.dribbles = row.find("td", attrs={"data-stat":"take_ons_won"}).contents[0]
        self.dribbles_attempted = row.find("td", attrs={"data-stat":"take_ons"}).contents[0]

    
    def fill_gk_stats (self,row):
        self.gk_stats_filled = True
        self.gk_sota = row.find("td", attrs={"data-stat":"gk_shots_on_target_against"}).contents[0]
        self.gk_ga = row.find("td", attrs={"data-stat":"gk_goals_against"}).contents[0]
        self.gk_saves = row.find("td", attrs={"data-stat":"gk_saves"}).contents[0]
        self.gk_psxg = row.find("td", attrs={"data-stat":"gk_psxg"}).contents[0]
        self.gk_launches_completed = row.find("td", attrs={"data-stat":"gk_passes_completed_launched"}).contents[0]
        self.gk_launches = row.find("td", attrs={"data-stat":"gk_passes_launched"}).contents[0]
        self.gk_passes = row.find("td", attrs={"data-stat":"gk_passes"}).contents[0]
        self.gk_thows = row.find("td", attrs={"data-stat":"gk_passes_throws"}).contents[0]
        self.gk_avg_pass_length = row.find("td", attrs={"data-stat":"gk_passes_length_avg"}).contents[0]
        self.gk_crosses = row.find("td", attrs={"data-stat":"gk_crosses"}).contents[0]
        self.gk_crosses_stopped = row.find("td", attrs={"data-stat":"gk_crosses_stopped"}).contents[0]
        self.gk_def_actions_outside_box = row.find("td", attrs={"data-stat":"gk_def_actions_outside_pen_area"}).contents[0]
        self.gk_avg_distance_def_actions = row.find("td", attrs={"data-stat":"gk_avg_distance_def_actions"}).contents[0]
                                        
    def find_id(self, all_players):
        
        matches = [ pl for pl in all_players if (match_names ( pl[-2].strip()+" "+pl[-1].strip(), self.name.strip()))]
        if len (matches) ==0:
            print ("[ERROR found %d matches]" % len (matches))
            return False
        if len (matches)>1:
            print ("[ERROR found %d matches] -> looking for exact match" % len (matches))
            matches = [ pl for pl in all_players if ( ( pl[-2].strip()+" "+pl[-1].strip() == self.name.strip()))]
            print ("[ERROR]                  -> Found: %s" % (" ".join(matches[0][2:])) ) 
        self.id = matches[0][0]
        return True
        
    def __str__ (self):
        return ("[%s] %s = Pos:%s min:%s g:%s xg:%s a:%s xa:%s" % (self.id, self.name, self.pos, self.min, self.goal, self.xg, self.assist, self.xa)) + (" SoTa:%s Saves:%s psxg:%s" % (self.gk_sota, self.gk_saves, self.gk_psxg) if self.gk_stats_filled == True else "")

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=2)




        
# -----------------------------------------
def load_players ():
    # format: ID, Role, Name, Surname
    players = None
    with open (_calciatrici) as csvfile:
        players = list (r for r in csv.reader (csvfile, delimiter = ','))
    return players
# -----------------------------------------
def fill_gk_stats (stats, gk_table):

    
    for gk in gk_table.tbody.find_all (["tr"]):
        gk_name = gk.th.a.contents[0]
        print ("Filling GK: %s" % gk_name)

        gk_stat = next ( pl for pl in stats if pl.name == gk_name)
        if gk_stat == None:
            print ("[ERROR] Not found")
        print ("> Matching with %s" % gk_stat)

        gk_stat.fill_gk_stats (gk)
        print ("> Filled: %s" % gk_stat)
    return stats
            
# -----------------------------------------
def get_stats (stats_table):
    print ("Getting stats")
    players_not_found = []
    max_rows = 100
    stats = []
    for irow, row in enumerate (stats_table.find_all(["tr"])):
        if irow> max_rows:
            break
        
        if  (row.th.has_attr("class") and  "over_header" in row.th.attrs["class"]):
            print ("Over Header")
            continue
        if (row.th.has_attr("scope") and row.th.attrs["scope"] == "col"):
            print ("Header scope col")
            continue
        if ((str(irow-2)+" Players") in row.find("th", attrs={"data-stat":"player"}).contents[0]):
            print ("trailer")
            continue

        this_pl = playerstat(row)
        print ("Row:\t%s" % this_pl.name)
        if not this_pl.find_id( all_players = _all_players):
            players_not_found.append( this_pl.name)


        stats.append (this_pl)

    if (len (players_not_found)!=0):
        print ("+++++ NOT FOUND LIST +++++")
        print (players_not_found)

    return stats


# -----------------------------------------

print ("Playground: MatchReport %s" % _url)

# get the summary stats table
# summary_table = parsed_html.body.findAll ("div", attrs={"class" : "table_container tabbed current", "id" : lambda l:l and ('_summary' in l)})

_all_players = load_players()

summary_table = parsed_html.body.find_all ("div", attrs={"class" : "table_container tabbed current", "id" : re.compile(".*_summary")})
home_summary_table = summary_table[0].table
away_summary_table = summary_table[1].table
home_summary_stats = get_stats (home_summary_table)
away_summary_stats = get_stats (away_summary_table)

gk_tables = parsed_html.body.find_all ("div", attrs={"class" : "table_container", "id" : re.compile("div_keeper_stats_.*")})
home_stats_with_gk = fill_gk_stats (home_summary_stats, gk_tables[0])
away_stats_with_gk = fill_gk_stats (away_summary_stats, gk_tables[1])

total_stats_with_gk = home_stats_with_gk+away_stats_with_gk

with open (_json_output, "w+") as jsonfile:
    jsonfile.write ("["+"\n".join( [player.toJSON() for player in total_stats_with_gk])+"]")
    


