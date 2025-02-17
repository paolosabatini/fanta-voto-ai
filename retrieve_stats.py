#!/usr/bin/env python3

'''
Setting up logging for the application
'''
import logging
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

'''
Import needed services
'''
from services.RetrieveService import RetrieveService
from utils.db.DbPlayerStats import DbPlayerStats

'''
Main function
'''
def main():
    arguments = get_option_parser()
    matchweek = arguments.matchweek
    logging.info("Starting retrieve of results for matchweek:\t%d" % matchweek)

    rs = RetrieveService ( matchweek = matchweek )
    rs.execute()
    list_of_player_stats_for_matchweek = rs.get_all_stats()
    list_of_errors = rs.get_all_errors()
    logging.info("\t -> N. player stats:\t%d" % len(list_of_player_stats_for_matchweek))
    logging.info("\t -> N. errors:      \t%d" % len(list_of_errors))

    success = store_stats( matchweek, list_of_player_stats_for_matchweek ) 
    logging.info ("Db updated: %s" % "SUCCESS" if success else "FAILED")
    
'''
Store stats
'''
def store_stats( matchweek, list_of_stats ):
    return DbPlayerStats().write_from_list_for_matchweek(matchweek, list_of_stats) \
        and DbPlayerStats().update_gk_stats_for_matchweek(matchweek, [gk for gk in list_of_stats if gk.pos == 'GK'])
    
'''
Argument parser
'''
def get_option_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-w", "--week", dest="matchweek",type=int,
                        help="Matchweek to get the results from",required=True)
    return parser.parse_args()
    

'''
Main executable
'''
if __name__ == '__main__':
    main()
