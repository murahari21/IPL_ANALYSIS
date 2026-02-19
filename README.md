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

# total runs per match
player_runs = deliveries_df.groupby('match_id')['batsman_runs'].sum().reset_index()
player_runs.columns = ['match_id', 'total_match_runs']

# total wickets per match
match_wickets = deliveries_df.groupby('match_id')['is_wicket'].sum().reset_index()
match_wickets.columns = ['match_id', 'total_wickets']


#  LOAD +
matches_df.to_sql("matches", engine, if_exists="replace", index=False)
deliveries_df.to_sql("deliveries", engine, if_exists="replace", index=False)
players_df.to_sql("players", engine, if_exists="replace", index=False)
match_summary.to_sql("match_summary", engine, if_exists="replace", index=False)

print("✅ Data Loaded Successfully!")


# Create Streamlit Dashboard

Create file dashboard.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/ipl_project")

st.title("🏏 IPL ANALYSIS DASHBOARD")

dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    ["Team Performance", "Match Insights"]
)

# ---------------- TEAM PERFORMANCE ----------------
if dashboard == "Team Performance":

    st.header("Team Performance")

    df = pd.read_sql("""
    SELECT winner, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY winner
    ORDER BY wins DESC
    """, engine)

    st.dataframe(df)
    st.bar_chart(df.set_index("winner"))

# ---------------- MATCH INSIGHTS ----------------
elif dashboard == "Match Insights":

    st.header("Match Insights")

    runs = pd.read_sql("""
    SELECT match_id, SUM(batsman_runs) as total_runs
    FROM deliveries
    GROUP BY match_id
    """, engine)

    st.metric("Average Runs Per Match", round(runs["total_runs"].mean(),2))

#  Run Dashboard
streamlit run dashboard.py


Browser will open → Dashboard ready 🎉

# Optional Charts Using Matplotlib
import matplotlib.pyplot as plt

season_runs = pd.read_sql("""
SELECT season, COUNT(*) as matches
FROM matches
GROUP BY season
""", engine)

plt.bar(season_runs['season'], season_runs['matches'])
plt.title("Matches per Season")
plt.show()
