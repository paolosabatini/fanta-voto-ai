#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


class MatchStats:
    def __init__(self, id):
        self.id = id
        self.home = str()
        self.away = str()
        self.goal_home = 0
        self.goal_away = 0
        self.xg_home = 0
        self.xg_away = 0
        self.possession_home = 0
        self.possession_away = 0
        self.pass_accuracy_home = 0
        self.pass_accuracy_away = 0
        self.sota_home = 0
        self.sota_away = 0
        self.saves_home = 0
        self.saves_away = 0
        self.fouls_home = 0
        self.fouls_away = 0
        self.corners_home = 0
        self.corners_away = 0
        self.crosses_home = 0
        self.crosses_away = 0
        self.tackles_home = 0
        self.tackles_away = 0
        self.interceptions_home = 0
        self.interceptions_away = 0
        self.clearances_home = 0
        self.clearances_away = 0
        self.offsides_home = 0
        self.offsides_away = 0

    
