# Install Required Packages

Open terminal in project folder and run:

pip install pandas sqlalchemy pymysql streamlit matplotlib


# Create MySQL Database

Open MySQL and run:

CREATE DATABASE ipl_project;

USE ipl_project;

# Create MySQL Tables


CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    season INT,
    team1 VARCHAR(50),
    team2 VARCHAR(50),
    venue VARCHAR(100),
    winner VARCHAR(50),
    match_date DATE
);


CREATE TABLE deliveries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    inning INT,
    over_no INT,
    ball INT,
    batsman_runs INT,
    bowler_runs INT,
    is_wicket INT,
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);


CREATE TABLE players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    team VARCHAR(50),
    role VARCHAR(50)
);




# ETL Script (Load CSV → Clean → Store in MySQL)
Create file etl.py
import pandas as pd
from sqlalchemy import create_engine

# DATABASE CONNECTION
engine = create_engine("mysql+pymysql://root:root@localhost/ipl_project")

# EXTRACT 
matches_df = pd.read_csv("matches.csv")

deliveries_df = pd.read_csv("deliveries.csv")

players_df = pd.read_csv("players.csv")

# TRANSFORM 
matches_df.fillna("Unknown", inplace=True)

deliveries_df.fillna(0, inplace=True)

players_df.fillna("Unknown", inplace=True)


matches_df['match_date'] = pd.to_datetime(matches_df['match_date'])

deliveries_df['batsman_runs'] = deliveries_df['batsman_runs'].astype(int)
deliveries_df['bowler_runs'] = deliveries_df['bowler_runs'].astype(int)
deliveries_df['is_wicket'] = deliveries_df['is_wicket'].astype(int)


#  LOAD Data
matches_df.to_sql("matches", engine, if_exists="replace", index=False)
deliveries_df.to_sql("deliveries", engine, if_exists="replace", index=False)
players_df.to_sql("players", engine, if_exists="replace", index=False)
match_summary.to_sql("match_summary", engine, if_exists="replace", index=False)

print("✅ Data Loaded Successfully!")


# IPL_ANALYSIS VISUALIZATION

# total runs per match
import matplotlib.pyplot as plt

plt.figure()
plt.hist(player_runs['total_match_runs'], bins=20)
plt.title("Runs Distribution per Match")
plt.xlabel("Total Runs in Match")
plt.ylabel("Number of Matches")
plt.show()

<img width="923" height="562" alt="image" src="https://github.com/user-attachments/assets/5f6ba0a3-42e6-45cb-8567-8b684b842d0c" />


# total wickets per match

import matplotlib.pyplot as plt

plt.figure()
plt.bar(match_wickets['match_id'], match_wickets['total_wickets'])
plt.title("Wickets per Match")
plt.xlabel("Match ID")
plt.ylabel("Total Wickets")
plt.show()

<img width="908" height="670" alt="image" src="https://github.com/user-attachments/assets/6c798e65-3f7f-4a01-afd1-9d6bddbe414a" />

# Season-wise Total Matches Chart
import matplotlib.pyplot as plt
season_matches = matches_df.groupby('season').size().reset_index(name='total_matches')

plt.figure()
plt.bar(season_matches['season'], season_matches['total_matches'])
plt.title("Season-wise Total Matches")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.show()

<img width="920" height="674" alt="image" src="https://github.com/user-attachments/assets/b90e020f-9008-4947-a0a8-f49a27ab76f4" />


# Average Runs Per Season
if 'season' not in match_summary.columns:
    match_summary = match_summary.merge(matches_df[['match_id','season']], on='match_id')

avg_runs_season = match_summary.groupby('season')['total_match_runs'].mean().reset_index()

plt.figure()
plt.bar(avg_runs_season['season'], avg_runs_season['total_match_runs'])
plt.title("Average Runs Per Season")
plt.xlabel("Season")
plt.ylabel("Average Runs")
plt.show()

<img width="959" height="681" alt="image" src="https://github.com/user-attachments/assets/e9bef1fa-ff2f-4b22-9616-4f79dc7ca7ba" />

# Total Runs Per Season
import matplotlib.pyplot as plt

 //Merge to get season
merged_df = deliveries_df.merge(
    matches_df[['match_id', 'season']],
    on='match_id'
)

// Total runs per season
season_runs = merged_df.groupby('season')['batsman_runs'].sum()

plt.figure(figsize=(8,5))
plt.plot(season_runs.index, season_runs.values)

plt.title("Total Runs Per Season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.show()

<img width="1031" height="656" alt="image" src="https://github.com/user-attachments/assets/58eb6d69-b37d-41d6-b2c8-4590d9ec90d9" />



# Top 5 Teams by Win Percentage

win_percentage = (total_wins / total_matches * 100).reset_index()
win_percentage.columns = ['team', 'win_percentage']

top5 = win_percentage.sort_values(by='win_percentage', ascending=False).head()

plt.figure()
plt.bar(top5['team'], top5['win_percentage'])
plt.xticks(rotation=45)
plt.title("Top 5 Teams by Win Percentage")
plt.ylabel("Win Percentage")
plt.xlabel("Teams")
plt.show()

<img width="858" height="640" alt="image" src="https://github.com/user-attachments/assets/4807977a-c5c5-4c8c-ba22-ecb4e2fe8926" />



# High Scoring Matches (>180 runs)

high_score = match_summary[match_summary['total_match_runs'] > 180]

plt.figure()
plt.bar(high_score['match_id'], high_score['total_match_runs'])
plt.title("High Scoring Matches (>180 Runs)")
plt.xlabel("Match ID")
plt.ylabel("Total Runs")
plt.show()


<img width="892" height="653" alt="image" src="https://github.com/user-attachments/assets/90fa6110-3d97-4167-9f70-0fa49da79a77" />




plt.title("Matches per Season")
plt.show()
