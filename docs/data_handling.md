Data handling 
-------------

This process consists of two steps: retrieving open source data and store them in a user-friendly format (data preparation) and pre-process the data to create the inputs for the model training (data pre-processing).

### Preparation

Three sources of open-access data are available, however they are very limited and contain limited information on players, teams and matches. References are the following:

- [Federazione Italiana Giuoco Calcio (FIGC)](https://www.figc.it/it/femminile/club/club-serie-a/): official web-site of the Italian football association. The (cumulative) statistics of each player are available, e.g. goals, shots, yellow/red cards etc..
- [Football Statistics and History (FBref)](https://fbref.com/en/comps/208/Serie-A-Stats): database collecting statistics on football. Only limited statistics are available on women italian league, such as fixtures and average team performances (e.g. average goals and assists per match). The amount of data on women italian football league is way smaller than the corresponding men's league. For example, individual statistics including `StatsBomb` expected goals are not available for free.
- [FantaWomen](https://www.lfootball.it/fantawomen/index.php): this is the source of the target evaluation (vote, mark) for each player each match that the machine should replicate.

These data are collected every matchweek (season 2022-2023) and stored in individual files. These files are combined and transformed in the pre-processing step. A short overview on the features and their possible importance in the mark estimation is given below.

##### Player position

The position (role) of the player on the pitch has a crucial role in the evaluation determination, as they depend on different features and they even span over different ranges. It is known that a good performance of a forward scoring a goal is easier to notice with respect to a defensive player, resulting in a higher average score. This would even reflect in making the mark estimation for defenders or midfielder harder and probably more accurate (and not available at the moment) features could be needed to correctly evaluate them.

_Do aggregate distributions for each position show this?_ Not really, most of the players plays mediocre, so that their evaluation (ranging from 0 to 10). 
