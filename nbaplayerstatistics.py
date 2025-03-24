#NbaPlayerStatistics (making a csv file to perform pca analysis)

from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.endpoints import PlayerCareerStats
from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.endpoints import CommonPlayerInfo
from nba_api.stats.static import players
import pandas as pd
import csv

def get_all_player_season_stats(season="2024-25"):
    season_player_stats = LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame").get_data_frames()[0]

    #check if data is empty
    if season_player_stats.empty:
        print(f"No player stats found for {season}")
        return

    print(f"\nStats for all Players for the {season} season")
    print(season_player_stats.head())

    #save to csv
    season_player_stats.to_csv(f'All_Players_season_{season}_Stats.csv', index=False)
    print(f"\nStats for all players for the {season} season saved to 'All_Players_Season_{season}_Stats.csv'")

get_all_player_season_stats(season="2024-25")


