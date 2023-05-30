import pandas as pd

class ProcessGameState:
    def __init__(self, file_path, boundary):
        self.file_path = file_path
        self.boundary = boundary

    def extract_data(self):
        data = pd.read_parquet(self.file_path, engine='pyarrow')
        return data
    
    def transform_data(self, original_data):
        # create a dictionary of each rounds' data with only Team 2
        data = {}
        # iterate over each row of data
        for (columnName, columnData) in original_data.iterrows():
            if columnData["team"] == "Team2":
                # get round number
                round_num = columnData["round_num"]
                # add round number to data if not already in there
                if round_num not in data:
                    data[round_num] = {}
                # add player to data if not already in there
                if columnData["player"] not in data[round_num]:
                    data[round_num][columnData["player"]] = []
                # append row to data[round_num][player]
                data[round_num][columnData["player"]].append(columnData)
        # sort each round's data by tick in ascending order
        for round_num_data in data:
            for player_data in data[round_num_data]:
                data[round_num_data][player_data].sort(key=lambda x: x["tick"])
        return data

    def load_data(self, transformed_data, output_file):
        transformed_data.to_parquet(output_file)

    def perform_etl(self, output_file):
        data = self.extract_data()
        transformed_data = self.transform_data(data)
        self.load_data(transformed_data, output_file)

    # extract weapon classes from data
    def extract_weapon_classes(self, data):
        weapon_classes = {}
        # iterate over each row of data
        for (columnName, columnData) in data.iterrows():
            # iterate through each item in inventory
            # None check for inventory
            if columnData["inventory"] is None:
                continue
            for item in columnData["inventory"]:
                # get weapon_class from item
                weapon_class = item["weapon_class"]
                # get weapon_name from item
                weapon_name = item["weapon_name"]
                # add weapon_class to weapon_classes if not already in there
                if weapon_class not in weapon_classes:
                    weapon_classes[weapon_class] = []
                # add weapon_name to weapon_class if not already in there
                if weapon_name not in weapon_classes[weapon_class]:
                    weapon_classes[weapon_class].append(weapon_name)
        print("----------------------------------------------------")
        print("Question 1c:")
        print("Extracted Weapon Class: ")
        print(weapon_classes)
        return weapon_classes
    
    def extract_area_name(self, data):
        area_names = {}
        for (columnName, columnData) in data.iterrows():
            area_name = columnData["area_name"]
            if area_name not in area_names:
                area_names[area_name] = 0
            area_names[area_name] += 1
        # print(area_names)
        return area_names
    
    # vertices must be consecutive
    def is_within_boundary(self, point, vertices):
        # Extract the coordinates of the point
        x, y, z = point
        n = len(vertices)
        inside = False
        
        p1x, p1y = vertices[0]
        for i in range(n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_intercept = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_intercept:
                                inside = not inside
            p1x, p1y = p2x, p2y
        return inside and z >= 285 and z <= 421
    

# Example usage
input_file = 'game_state_frame_data.parquet'
output_file = 'output.parquet'

# Create an instance of the ProcessGameState class
boundary = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
processor = ProcessGameState(input_file, boundary)

# Perform the ETL job and save the output to the specified file
data = processor.extract_data()
processor.transform_data(data)