```mermaid 
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
