import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/ipl_project")

matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
players = pd.read_csv("players.csv")

# rename column "over" because it is reserved word in MySQL
deliveries.rename(columns={"over": "over_no"}, inplace=True)

matches.to_sql("matches", engine, if_exists="replace", index=False)
deliveries.to_sql("deliveries", engine, if_exists="replace", index=False)
players.to_sql("players", engine, if_exists="replace", index=False)


print("Data loaded successfully!")
