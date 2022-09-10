**Don't you want/can watch all matches on Sunday to give votes to players?** Just relax and let the machine do it!

This is designed to provide - _in the future_ - automatic evaluation of Serie A Women players each matchweek to be used by the [FantaWomen](https://www.lfootball.it/fantawomen/index.php). Even better, in a perfect future with _live_ statistics for players, we could give _live_ evaluations!

This web-page has just the scope of logbook (for me to keep tracks of tests/conclusions) and code/models documentations.

Documentation
-------------

Below a simple diagram of the code structure, click on the boxes to access the documentation. Blocks in red are not ready/implemented.

```mermaid!
flowchart LR
  subgraph "Data handling"
  figc[FIGC website] --> dp[Data preparation]
  fbref[FBREF website] --> dp[Data preparation]
  db[Database] --> dp[Data preparation]
  dp[Data preparation] == JSON ==> pp[Pre-processing] 
  end
  subgraph "Machine Learning"
  pp[Pre-processing]  == pickle ==> training[Model training] 
  training[Model training]  ==> eval[Model evaluation]
  eval[Model evaluation] -- tuning --> training[Model training]
  end
  
  style training fill:#ff0000,stroke:#333,stroke-width:0px
  style eval fill:#ff0000,stroke:#333,stroke-width:0px

  click figc "https://www.figc.it/it/femminile/" _blank
  click fbref "https://fbref.com/en/" _blank
  click db "https://fbref.com/en/" _blank
```

The list of models with performance are documented by clicking the model training and evaluation blocks.
