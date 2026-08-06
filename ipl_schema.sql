CREATE DATABASE IF NOT EXISTS ipl_db;
USE ipl_db;

CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    season INT,
    match_date DATE,
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    winner VARCHAR(100),
    venue VARCHAR(150),
    toss_winner VARCHAR(100),
    toss_decision VARCHAR(20),
    result VARCHAR(30),
    player_of_match VARCHAR(100)
);

CREATE TABLE deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    inning INT,
    over_no INT,
    ball_no INT,
    batsman VARCHAR(100),
    bowler VARCHAR(100),
    batsman_runs INT,
    extra_runs INT,
    total_runs INT,
    is_wicket INT,
    dismissal_kind VARCHAR(50),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    team VARCHAR(100),
    role VARCHAR(50)
);
