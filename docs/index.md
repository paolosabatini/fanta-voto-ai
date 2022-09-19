**Don't you want/can watch all matches on Sunday to give votes to players?** Just relax and let the machine do it!

This is designed to provide - _in the future_ - automatic evaluation of Serie A Women players each matchweek to be used by the [FantaWomen](https://www.lfootball.it/fantawomen/index.php). Even better, in a perfect future with _live_ statistics for players, we could give _live_ evaluations!

This web-page has just the scope of logbook (for me to keep tracks of tests/conclusions) and code/models documentations.

Documentation
-------------

Below a simple diagram of the code structure, click on the boxes to access the documentation. Blocks in red are not ready/implemented.

__EDIT:__ unfortunately `mermaid diagrams` __are not__ supported by `gh-pages` at the moment. The diagram is now converted in a static image and links are not working. Links to the documentations is provided below.

![Diagram (last update: 19/09/2022)](./img/scheme_220919.png)

The list of models with performance are documented by clicking the model training and evaluation blocks.

### Data handling

This step consists in retrieving the information available on the web - _for free_ - and processing it as input to the machine learning algorithm.

[_Click here to discover the data!_](data_handling.md)

### Models

Several models have been tested for this analysis, starting from the easiest ones to the more complex. All the models tested, with the corresponding performance studies, are documented in the link below.

- [K-neighbours regressor](kneigh_kf5.md): easiest model, and not machine learning at all. Just a sort-of look-up table from the available dataset in input.
