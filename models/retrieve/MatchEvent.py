#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


from copy import deepcopy

class MatchEvent:

    player = str()
    event_type = str()
    
    def __init__ (self, row):
        self.event_type = self.get_event_type (row)
        match self.event_type:
            case "sub":
                self.init_sub_event(row)
            case "yellow_card":
                self.init_card_event(row)
            case "red_card":
                self.init_card_event(row)
            case "goal":
                self.init_goal_event(row)
            case "own_goal":
                self.init_own_goal_event(row)
            case "pen_failed":
                self.init_pen_failed_event(row)
            case _:
                return

    def init_sub_event(self, event_row):
        self.player_in = event_row.findAll("div")[3].div.a.contents[0]
        self.player_out = event_row.findAll("div")[3].small.a.contents[0]
        logging.debug ("SUB IN: %s | OUT: %s" % (self.player_in, self.player_out))

    def init_card_event(self, event_row):
        self.player = event_row.findAll("div")[3].a.contents[0]
        logging.debug ("CARD [%s] for %s" % (self.event_type, self.player))

    def init_goal_event(self, event_row):
        self.player = event_row.findAll("div")[3].a.contents[0]
        try:
            self.assist = event_row.findAll("div")[3].small.a.contents[0]
            logging.debug ("GOAL of %s (A: %s)" % (self.player, self.assist))
        except:
            logging.debug ("GOAL of %s (no assist)" % (self.player))

    def init_own_goal_event(self, event_row):
        self.player = event_row.findAll("div")[3].a.contents[0]
        logging.debug ("OWN GOAL of %s" % (self.player))

    def init_pen_failed_event(self, event_row):
        self.player = event_row.findAll("div")[3].a.contents[0]
        try:
            self.saved = event_row.findAll("div")[3].small.a.contents[0]
            logging.debug ("PEN FAILED by %s (saved by %s)" % (self.player, self.saved))
        except:
            logging.debug ("PEN FAILED by %s" % (self.player))
 

    def get_event_type (self,event_row):
        if len (event_row.findAll("div", attrs={"class":"event_icon substitute_in"})) != 0:
            return "sub"
        elif len (event_row.findAll("div", attrs={"class":"event_icon yellow_card"})) != 0:
            return "yellow_card"
        elif len (event_row.findAll("div", attrs={"class":"event_icon red_card"})) != 0:
            return "red_card"
        elif len (event_row.findAll("div", attrs={"class":"event_icon goal"})) != 0:
            return "goal"
        elif len (event_row.findAll("div", attrs={"class":"event_icon penalty_goal"})) != 0:
            return "goal"
        elif len (event_row.findAll("div", attrs={"class":"event_icon own_goal"})) != 0:
            return "own_goal"
        elif len (event_row.findAll("div", attrs={"class":"event_icon penalty_miss"})) != 0:
            return "pen_failed"
        else:
            logging.warning ("[warning] found en event that is not understood!")
            return "unknown"

    
