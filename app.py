


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ---------------- DATABASE CONNECTION ----------------
engine = create_engine("mysql+pymysql://root:root@localhost/ipl_project")

# ---------------- PAGE TITLE ----------------
st.title("🏏 IPL ANALYSIS DASHBOARD")

# ---------------- SIDEBAR ----------------
dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Team Performance",
        "Match Insights",
        "Player & Ball Analytics",
        "Business KPIs"
    ]
)

# =====================================================
# 🔹 DASHBOARD 1 : TEAM PERFORMANCE
# =====================================================

if dashboard == "Team Performance":

    st.header("Team Performance Analysis")

    # Highest Wins
    st.subheader("Highest Wins Across Seasons")

    query1 = """
    SELECT winner, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY winner
    ORDER BY wins DESC;
    """
    df1 = pd.read_sql(query1, engine)

    st.dataframe(df1)
    st.bar_chart(df1.set_index("winner"))


    # Wins by Venue
    st.subheader("Wins by Venue")

    query2 = """
    SELECT venue, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY venue
    ORDER BY wins DESC;
    """
    df2 = pd.read_sql(query2, engine)

    st.dataframe(df2)


    # Season-wise Dominance
    st.subheader("Season-wise Team Dominance")

    query3 = """
    SELECT season, winner, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY season, winner
    ORDER BY season;
    """
    df3 = pd.read_sql(query3, engine)

    st.dataframe(df3)



# =====================================================
# 🔹 DASHBOARD 2 : MATCH INSIGHTS
# =====================================================

elif dashboard == "Match Insights":

    st.header("Match Insights")

    # Average Runs Per Match
    st.subheader("Average Runs Per Match")

    query1 = """
    SELECT match_id, SUM(batsman_runs) as total_runs
    FROM deliveries
    GROUP BY match_id;
    """
    df_runs = pd.read_sql(query1, engine)

    avg_runs = df_runs["total_runs"].mean()
    st.metric("Average Runs Per Match", round(avg_runs, 2))


    # Matches with No Result
    st.subheader("Matches with No Result")

    query2 = """
    SELECT COUNT(*) as no_result
    FROM matches
    WHERE winner IS NULL;
    """
    df2 = pd.read_sql(query2, engine)

    st.metric("No Result Matches", df2.iloc[0]["no_result"])


    # Home vs Away Performance
    st.subheader("Home vs Away Performance")

    query3 = """
    SELECT team1, COUNT(*) as matches_played
    FROM matches
    GROUP BY team1;
    """
    df3 = pd.read_sql(query3, engine)

    st.dataframe(df3)



# =====================================================
# 🔹 DASHBOARD 3 : PLAYER & BALL ANALYTICS
# =====================================================

elif dashboard == "Player & Ball Analytics":

    st.header("Player & Ball Analytics")

    # Runs Distribution
    st.subheader("Runs Distribution Per Match")

    query1 = """
    SELECT match_id, SUM(batsman_runs) as total_runs
    FROM deliveries
    GROUP BY match_id;
    """
    df1 = pd.read_sql(query1, engine)

    st.bar_chart(df1.set_index("match_id"))


    # Wickets Per Match
    st.subheader("Wickets Per Match")

    query2 = """
    SELECT match_id, SUM(is_wicket) as total_wickets
    FROM deliveries
    GROUP BY match_id;
    """
    df2 = pd.read_sql(query2, engine)

    st.bar_chart(df2.set_index("match_id"))


    # High Scoring Matches
    st.subheader("High Scoring Matches (>180 Runs)")

    high_score = df1[df1["total_runs"] > 180]
    st.dataframe(high_score)



# =====================================================
# 🔹 DASHBOARD 4 : BUSINESS KPIs
# =====================================================

elif dashboard == "Business KPIs":

    st.header("Business KPIs")

    # Top 5 Teams
    st.subheader("Top 5 Teams by Wins")

    query1 = """
    SELECT winner, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY winner
    ORDER BY wins DESC
    LIMIT 5;
    """
    df1 = pd.read_sql(query1, engine)

    st.dataframe(df1)
    st.bar_chart(df1.set_index("winner"))


    # Venue Impact
    st.subheader("Impact of Venue on Results")

    query2 = """
    SELECT venue, winner, COUNT(*) as wins
    FROM matches
    WHERE winner IS NOT NULL
    GROUP BY venue, winner
    ORDER BY venue;
    """
    df2 = pd.read_sql(query2, engine)

    st.dataframe(df2)


