
# SWE Intern Assessment

CounterStrike game strategies analysis on Bombsite B. Created by Mingming Zheng. Last updated on May 30th, 2023.




## Tasks

1. Write a python class ProcessGameState that will:
    - Handle file ingestion and ETL
        
        I implemented the Extract, Transform, Load (ETL) process by importing parquet data and organizing the Team 2 data into a Python dictionary. The dictionary has a hierarchical structure consisting of round numbers, player names, and rows. The function headers are displayed as follows:
        ```python 
        def extract_data(self):
        def transform_data(self, original_data):
        def load_data(self, transformed_data,output_file):
        ```
    - Return whether or not each row falls within a provided boundary
        
        I have implemented a function that utilizes the Ray Casting algorithm to check if a given point resides within a polygon. Then add a z axies check upon x and y.
        [reference](https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html)
    - Extract the weapon classes from the inventory
        
        I implemented a loop to iterate over every row of data and each item in the inventory. If the weapon class had not been encountered before, I initiated a new list. Afterwards, I assigned the weapon name to the corresponding weapon class to create a comprehensive list.
        ```python
        for item in columnData["inventory"]:
            weapon_class = item["weapon_class"]
            weapon_name = item["weapon_name"]
            if weapon_class not in weapon_classes:
                weapon_classes[weapon_class] = []
            if weapon_name not in weapon_classes[weapon_class]:
                weapon_classes[weapon_class].append(weapon_name)
        ```
        Program Result:
        ```bash
        Question 1c:
        Extracted Weapon Class: 
        {'Pistols': ['Glock-18', 'Tec-9', 'Desert Eagle', 'USP-S', 'Five-SeveN', 'P250', 'Dual Berettas'], 
        'Grenade': ['Decoy Grenade', 'Flashbang', 'Smoke Grenade', 'Molotov', 'Incendiary Grenade', 'HE Grenade'], 
        'Rifle': ['AK-47', 'Galil AR', 'M4A1', 'AWP', 'FAMAS', 'SG 553', 'SSG 08'], 'SMG': ['MP9']}
        ```
2. Using the created class, answer the following questions:
    - Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?
        
        As result shows, entering via the light blue boundary is not a common strategy by Team 2 on T side. Out of the 19 instances they crossed the light blue boundary, only 2 times did they manage to reach Bombsite B successfully.
        
        Program Result:
        ```bash
        Question 2a:
        Total number of times reaching Bombsite B via the light blue boundary:  2
        Total number of times passing the boundary:  19
        Frequency of entering via the light blue boundary:  0.11764705882352941
        ```
    - What is the average timer that Team2 on T (terrorist) side enters “BombsiteB” with least 2 rifles or SMGs?

        According to the findings, Team 2 typically takes approximately 29 seconds to successfully enter Bombsite B. This was determined by a function that filters the T side and considers only instances when players are alive. The function calculates the timer based on the "seconds" field in the raw data and also adjusts for time added when the seconds reset due to bomb planting. To determine if the Team is entering Bombsite B, the function checks the previous and current area names.
        ```bash
        Question 2b:
        average timer enters BombsiteB with least 2 rifles or SMGs:  29.0  seconds
        ```
    - Now that we’ve gathered data on Team2 T side, let's examine their CT(counter-terrorist) Side. Using the same data set, tell our coaching staff where you suspect them to be waiting inside “BombsiteB".
        
        To fulfill this request, multiple libraries have been imported to facilitate the creation of a heat map. The function filters the data to focus on players located within the Bombsite B area and extracts their respective x and y coordinates. It then creates a map where the keys are defined as (x, y) coordinates and the values represent the number of occurrences associated with each coordinate pair.
        
        Program Result:
        
        ![heat map](https://raw.githubusercontent.com/kumashi7/Evil-Geniuses-SDE-Intern-Assessment/master/heatmap.png)

        ### Complete program result
        ```base
        ----------------------------------------------------
        Game Analysis:
        ----------------------------------------------------
        Question 1c:
        Extracted Weapon Class: 
        {'Pistols': ['Glock-18', 'Tec-9', 'Desert Eagle', 'USP-S', 'Five-SeveN', 'P250', 'Dual Berettas'], 
        'Grenade': ['Decoy Grenade', 'Flashbang', 'Smoke Grenade', 'Molotov', 'Incendiary Grenade', 'HE Grenade'], 
        'Rifle': ['AK-47', 'Galil AR', 'M4A1', 'AWP', 'FAMAS', 'SG 553', 'SSG 08'], 'SMG': ['MP9']}
        ----------------------------------------------------
        Question 2a:
        Total number of times reaching Bombsite B via the light blue boundary:  2
        Total number of times passing the boundary:  19
        Frequency of entering via the light blue boundary:  0.11764705882352941
        ----------------------------------------------------
        Question 2b:
        average timer enters BombsiteB with least 2 rifles or SMGs:  29.0  seconds
        ----------------------------------------------------
        Question 2c
        Please see the poped up heatmap
        ```
        
3. Propose a solution to your product manager that:
    - could allow our coaching staff to request or acquire the output themselves
    - takes less than 1 weeks worth of work to implement

        I propose the development of a user-friendly interface for our backend Python file. To expedite the implementation process, we can utilize templates or libraries that offer pre-built components and functionality. Two suitable options for Python stack frameworks are Django and Flask.

By incorporating a user interface, we can create portals through which the coaching staff can easily input parameters or select pre-defined options to generate the desired output. The complete stack will not only fulfill the current request but also provide scalability for potential future deployments, accommodating increased user access.

To streamline backend development, it is advisable to adopt a modular approach and prioritize the implementation of core features. This approach enables us to expedite development while maintaining flexibility for accommodating new analysis requests through organized data transformations.

Implementing the proposed stack for our existing product can be achieved within a timeframe of less than one week.


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Run game analysis file

```bash
  python3 game_analysis.py
```


## 🚀 Thank you
Please contact me if there are any questions.


