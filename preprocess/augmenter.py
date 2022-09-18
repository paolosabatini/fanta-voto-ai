#!/usr/bin/env python

        
    
def goal_scored ( df ):
    df['goal_scored'] = df.apply (lambda x : x['goal_away'] if x['Squadra'] == x['away'] else x['goal_home'], axis=1)

    
def goal_taken ( df ):
    df['goal_taken'] = df.apply (lambda x : x['goal_away'] if x['Squadra'] == x['home'] else x['goal_home'], axis=1)

def this_goals_per90 ( df ):
    df['this_goals_per90'] = df.apply (lambda x : x['goals_per90'] if x['Squadra'] == x['home'] else x['goals_per90_away'], axis=1)

def opponent_goals_per90 ( df ):
    df['opponent_goals_per90'] = df.apply (lambda x : x['goals_per90'] if x['Squadra'] == x['away'] else x['goals_per90_away'], axis=1)

def this_goals_pens_per90 ( df ):
    df['this_goals_pens_per90'] = df.apply (lambda x : x['goals_pens_per90'] if x['Squadra'] == x['home'] else x['goals_pens_per90_away'], axis=1)

def opponent_goals_pens_per90 ( df ):
    df['opponent_goals_pens_per90'] = df.apply (lambda x : x['goals_pens_per90'] if x['Squadra'] == x['away'] else x['goals_pens_per90_away'], axis=1)

def this_assists_per90 ( df ):
    df['this_assists_per90'] = df.apply (lambda x : x['assists_per90'] if x['Squadra'] == x['home'] else x['assists_per90_away'], axis=1)

def opponent_assists_per90 ( df ):
    df['opponent_assists_per90'] = df.apply (lambda x : x['assists_per90'] if x['Squadra'] == x['away'] else x['assists_per90_away'], axis=1)

def other_team (df):
    df ['other_team'] = df.apply (lambda x: x['away'] if x['Squadra'] == x['home'] else x['home'], axis=1)

def total_shots_made ( df ):
    feature_table = df.groupby (["home","away","Squadra"], as_index=False)['Tiri'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,  on = ["home","away","Squadra"], suffixes = ['','_Totali']).set_index("index")
    df ['total_shots_made'] = merged_with_feature ['Tiri_Totali']

    
def total_shots_taken ( df ):
    other_team (df)
    
    feature_table = df.groupby (["home","away","other_team"], as_index=False)['Tiri'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,
                                                  left_on = ["home","away","Squadra"],
                                                  right_on = ["home","away","other_team"],
                                                  suffixes = ['','_Totali']).set_index("index")
    df ['total_shots_taken'] = merged_with_feature ['Tiri_Totali']

    df.drop (['other_team'], axis=1)


def total_shots_on_target_made ( df ):
    feature_table = df.groupby (["home","away","Squadra"], as_index=False)['Tiri_in_porta'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,  on = ["home","away","Squadra"], suffixes = ['','_Totali']).set_index("index")
    df ['total_shots_on_target_made'] = merged_with_feature ['Tiri_in_porta_Totali']

    
def total_shots_on_target_taken ( df ):
    other_team (df)
    
    feature_table = df.groupby (["home","away","other_team"], as_index=False)['Tiri_in_porta'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,
                                                  left_on = ["home","away","Squadra"],
                                                  right_on = ["home","away","other_team"],
                                                  suffixes = ['','_Totali']).set_index("index")
    df ['total_shots_on_target_taken'] = merged_with_feature ['Tiri_in_porta_Totali']

    df.drop (['other_team'], axis=1)

    
def total_fouls_made ( df ):
    feature_table = df.groupby (["home","away","Squadra"], as_index=False)['Falli_commessi'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,  on = ["home","away","Squadra"], suffixes = ['','_Totali']).set_index("index")
    df ['total_fouls_made'] = merged_with_feature ['Falli_commessi_Totali']


def total_fouls_taken ( df ):
    feature_table = df.groupby (["home","away","Squadra"], as_index=False)['Falli_subiti'].agg ('sum')
    merged_with_feature = df.reset_index().merge (how="left", right=feature_table,  on = ["home","away","Squadra"], suffixes = ['','_Totali']).set_index("index")
    df ['total_fouls_taken'] = merged_with_feature ['Falli_subiti_Totali']
