use fantavoto_ai;

LOAD DATA LOCAL INFILE './Calciatrici.csv'
INTO TABLE players
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n';
