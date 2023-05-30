from process_game_state import ProcessGameState
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

input_file = 'game_state_frame_data.parquet'

# Create an instance of the ProcessGameState class
boundary = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
processor = ProcessGameState(input_file, boundary)
data = processor.extract_data()
processed_data = processor.transform_data(data)

def boomsite_b_enter_strategy(raw_data):
    # iterate over data by round and player
    current_loc = ""
    passed_light_blue = False
    num_reach_b_after_pass_through = 0
    total_pass_target_area = 0
    reach_b = 0
    data = raw_data.copy()
    for round_num in data:
        # get first player's side
        player_key = list(data[round_num].keys())[0]
        if data[round_num][player_key][0]["side"] == "CT":
            continue
        for player in data[round_num]:
            for row in data[round_num][player]:
                if not row["is_alive"]:
                    break
                if processor.is_within_boundary((row['x'], row['y'], row['z']), boundary):
                    passed_light_blue = True
                    total_pass_target_area += 1

                # get current location
                current_loc = row["area_name"]
                if current_loc == "BombsiteB":
                    if passed_light_blue:
                        num_reach_b_after_pass_through += 1
                        passed_light_blue = False      
    for round_num in data:
        # get first player's side
        player_key = list(data[round_num].keys())[0]
        if data[round_num][player_key][0]["side"] == "CT":
            continue
        for player in data[round_num]:
            for row in data[round_num][player]:
                if not row["is_alive"]:
                    break
                # get current location
                current_loc = row["area_name"]
                if current_loc == "BombsiteB":
                    reach_b += 1
                    break
    print("----------------------------------------------------")
    print("Question 2a:")
    print("Total number of times reaching Bombsite B via the light blue boundary: ", num_reach_b_after_pass_through)
    print("Total number of times passing the boundary: ", total_pass_target_area)  
    print("Frequency of entering via the light blue boundary: ", num_reach_b_after_pass_through / reach_b)

def bomebsite_b_timer(data):
    # only when player is alive and reach b and team has two more players in B with rifles or SMGs
    all_time = []
    for round_num in data:
        # get first player's side
        reach_b_timer = {}
        player_key = list(data[round_num].keys())[0]
        if data[round_num][player_key][0]["side"] == "CT":
            continue
        for player in data[round_num]:
            enter_b = False
            start_time = 0
            end_time = 0
            prev_sec = 0
            bomb_plant_time = 0
            for row in data[round_num][player]:
                current_sec = row["seconds"]
                if row["bomb_planted"]:
                    bomb_plant_time = prev_sec
                else:
                    prev_sec = current_sec
                if not row["is_alive"]:
                    if current_loc != "BombsiteB" and enter_b:
                        enter_b = False
                        end_time = row["seconds"]
                        if player not in reach_b_timer:
                            reach_b_timer[player] = []
                        reach_b_timer[player].append((start_time, end_time))
                    break
                current_loc = row["area_name"]
                if current_loc == "BombsiteB" and not enter_b:
                    for item in row["inventory"]:
                        # get weapon_class from item
                        weapon_class = item["weapon_class"]
                        if weapon_class == "Rifle" or weapon_class == "SMG":
                            enter_b = True
                            start_time = row["seconds"] + bomb_plant_time
                            break
                        else:
                            continue
                if current_loc != "BombsiteB" and enter_b:
                    enter_b = False
                    end_time = row["seconds"] + bomb_plant_time
                    if player not in reach_b_timer:
                        reach_b_timer[player] = []
                    reach_b_timer[player].append((start_time, end_time))
        if (len(reach_b_timer) > 1):
            all_time.append(first_double_enter_b_time(reach_b_timer))
    print("----------------------------------------------------")
    print("Question 2b:")
    print("average timer enters BombsiteB with least 2 rifles or SMGs: ", \
          sum(all_time) / len(all_time), " seconds")
        
def first_double_enter_b_time(reach_b_timer):
    min_time = 100000
    for player in reach_b_timer:
        for other_player in reach_b_timer:
            if player == other_player:
                continue
            for time in reach_b_timer[player]:
                start_time, end_time = time
                for other_time in reach_b_timer[other_player]:
                    other_start_time, other_end_time = other_time
                    if start_time < other_end_time or end_time > other_start_time:
                        min_time = min(min_time, min(start_time, other_start_time))
    return min_time

def boomsite_b_heat_map(data):
    heat_map = {} # key: (x, y), value: num of times
    # iterate over data by round and player
    for round_num in data:
        # get first player's side
        player_key = list(data[round_num].keys())[0]
        if data[round_num][player_key][0]["side"] == "T":
            continue
        for player in data[round_num]:
            for row in data[round_num][player]:
                if not row["is_alive"]:
                    break
                # get current location
                current_loc = row["area_name"]
                if current_loc == "BombsiteB":
                    x = row["x"] // 10 * 10
                    y = row["y"] // 10 * 10
                    if (x, y) not in heat_map:
                        heat_map[(x, y)] = 0
                    heat_map[(x, y)] += 1
    ser = pd.Series(list(heat_map.values()),
                  index=pd.MultiIndex.from_tuples(heat_map.keys()))
    df = ser.unstack().fillna(0)
    sns.heatmap(df)
    print("----------------------------------------------------")
    print("Question 2c")
    print("Please see the poped up heatmap")
    plt.show()

# generate entire game analysis for bombsite b
print("----------------------------------------------------")
print("Game Analysis:")
processor.extract_weapon_classes(data)
boomsite_b_enter_strategy(processed_data)
bomebsite_b_timer(processed_data)
boomsite_b_heat_map(processed_data)