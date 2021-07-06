from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonallplayers
import time
import pandas as pd
#from nba_api.stats.endpoints import cumestatsteam
from nba_api.stats.endpoints import playercareerstats


# Find teams by full name.
#print(teams.find_teams_by_full_name('cav'))

## Find teams by state.
#teams.find_teams_by_state('ohio')
#
## Find teams by city.
#teams.find_teams_by_city('cleveland')
#
## Find teams by team nickname.
#teams.find_teams_by_nickname('cav')
#
## Find teams by year founded.
#teams.find_teams_by_year_founded(1968)
#
## Find teams by abbreviation.
#teams.find_team_by_abbreviation('cle')
#
## Find teams by id.
#teams.find_team_name_by_id(1610612739)
#
## Get all teams.
#all_teams = teams.get_teams()

#for team in all_teams:
#    print(team)

    
def get_data(player):
    p_id = player['id']
    player_name = player['full_name']
#    print(player)
    career = playercareerstats.PlayerCareerStats(player_id=p_id)
    player_df = pd.DataFrame(career.get_data_frames()[0], columns=['PLAYER_ID', 'SEASON_ID', 'TEAM_ID', 'PTS'])
    time.sleep(2)
    player_df['Name'] = player_name
#    print(player_df.values.tolist())
    return player_df.values.tolist()
    
#all_players = players.get_players()[3653::]
#print(len(all_players))
#index = 0
#for player in all_players:
#    if player['full_name'] == 'Cedric Simmons':
#        print(index)
#    index += 1
#    print(player['full_name'])
#    
#    p_id = player['id']
#    player_name = player['full_name']
#    print(player)
#    career = playercareerstats.PlayerCareerStats(player_id=p_id)
#    player_df = pd.DataFrame(career.get_data_frames()[0], columns=['PLAYER_ID', 'SEASON_ID', 'TEAM_ID', 'PTS'])
#    time.sleep(2)
#    player_df['Name'] = player_name
#    print(player_df.values.tolist())

    
#def get_player_data()

#all_players = players.get_players()
##print(all_players)
#for player in all_players:
#    player_id = player['id']
#    player_info = commonallplayers.CommonAllPlayers(is_only_current_season=0, league_id="00", season=2019-20)
#    print(player_info.get_dict())
#    team_shit = teamdetails.TeamDetails()
#        print()
#    print(player_id)
#    player_info = 
#    print(player_info.get_dict())
#    player_info = commonplayerinfo.CommonPlayerInfo(player_id)
#    print(player_info.get_dict())
#print(players.get_players()[0])