use fantavoto_ai

CREATE TABLE player_stats (
Matchweek int NOT NULL,
ID int NOT NULL,
Name varchar(255),
Position varchar(255),
Minutes int,
Goals int,
Assists int,
Pens int,
Pens_attempted int,
Shots int,
Shots_on_target int,
Yellow_card int,
Red_card int,
Touches int,
Intercepts int,
Blocks int,
XG float,
NPXG float,
XA float,
SCA float,
GCA float,
Pass_completed int,
Pass_attempted int,
Progressive_pass int,
Carries int,
Progressive_carries int,
Dribbles int,
Dribbles_attempted int,
GK_sota int,
GK_GA int,
GK_saves int,
GK_PSXG int,
GK_launches_completed int,
GK_passes int,
GK_throws int,
GK_avg_pass_length int,
GK_crosses int,
GK_crosses_stopped int,
GK_def_actions_outside_box int,
GK_avg_distance_def_actions float
);

ALTER TABLE player_stats ADD UNIQUE player_stats_index (`Matchweek`, `ID`);

CREATE TABLE players (
ID int NOT NULL UNIQUE,
Position char NOT NULL,
Name varchar(255) NOT NULL,
Surname varchar(255) NOT NULL
);
