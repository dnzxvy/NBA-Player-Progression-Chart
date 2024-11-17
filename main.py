#Player Developement Tracker
from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.endpoints import PlayerCareerStats
from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.endpoints import CommonPlayerInfo
from nba_api.stats.static import players
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def get_player_id(player_name):
    # Find the player by name
    player_list = [player for player in players.get_players() if player_name.lower() in player['full_name'].lower()]

    if player_list:
        # Return the first matching player's ID
        return player_list[0]['id']
    else:
        raise ValueError("Player not found. Please check the player name.")

def plot_player_stats(player_name):
    player_id = get_player_id(player_name)
    all_time_player_stats = PlayerCareerStats(player_id=player_id, per_mode36="PerGame").get_data_frames()[0]

    player_info = CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
    player_name = player_info.loc[0, "DISPLAY_FIRST_LAST"]

    print("Available columns in the DataFrame: ")
    print(all_time_player_stats.columns)

    print("\nFirst few rows of player stats: ")
    print(all_time_player_stats.head())


    #Display the results

    print(f"\nCareer Stats of {player_name} ")
    print(all_time_player_stats)

    #save to csv
    all_time_player_stats.to_csv('PlayerProgression.csv', index=False)
    print("\nJoker stats saved to 'PlayerProgression.csv'")

    all_time_player_stats['SEASON_ID'] = all_time_player_stats['SEASON_ID'].str[:4].astype(int)




    seasons = all_time_player_stats['SEASON_ID']
    points = all_time_player_stats['PTS']


    fig, ax = plt.subplots(figsize=(20, 8))
    ax.set_xlim(seasons.min(), seasons.max() + 5) #x-axis for seasons.
    ax.set_ylim(0, points.max() + 5) #y-axis for ppg

    line, = ax.plot([], [], color='blue', marker='o') #initialises an empty plot
    ax.set_title(f"{player_name} Career PPG")
    ax.set_xlabel("Season")
    ax.set_ylabel("Points per game")


    def update(frame):

        x = seasons[:frame]
        y = points[:frame]
        line.set_xdata(seasons[:frame])
        line.set_ydata(points[:frame])
        return line,

    #return line, #comma required by FuncAnimation to make sure tuple is returned

    #create animation

    ani = FuncAnimation(fig=fig, func=update, frames=len(seasons), interval=700)

    # Create the animation:
    # - 'update' is the function that will update the plot for each frame
    # - 'frames' is the number of frames (i.e., the length of the 'seasons' data)
    # - 'interval' controls how fast the frames are displayed (500 ms between frames)
    # - 'blit=True' optimizes the animation by only redrawing the parts of the plot that change

    plt.grid(True)
    plt.show()

player_name = input("Enter the player name to see their career stats and plot: ")

try:
    plot_player_stats(player_name)
except Exception as e:
    print(f"Error: {e}. please check player id.")