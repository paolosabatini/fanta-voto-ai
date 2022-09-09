#!/usr/bin/env python

        
    
def goal_scored ( df ):
    df['goal_scored'] = df.apply (lambda x : x['goal_away'] if x['Squadra'] == x['away'] else x['goal_home'], axis=1)

    
def goal_taken ( df ):
    df['goal_taken'] = df.apply (lambda x : x['goal_away'] if x['Squadra'] == x['home'] else x['goal_home'], axis=1)


    
    
