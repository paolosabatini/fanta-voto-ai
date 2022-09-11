# fanta-voto-ai
ML algorithm to estimate the vote for FantaWomen based on available data. More documentation in the dedicated [web-page](https://paolosabatini.github.io/fanta-voto-ai/).

## Plug & play recipes

Here are the commands to plug and play the code, at the moment only data-preparation and pre-processing infrastructures are ready.

### Data preparation

To launch the data-preparation, you need only to write the following command:

```
./prepare_data
```

This will read the configuration in `dataprep/conf.py` and read the corresponding data. Everything is exported to `json` files in `data/` folder. In case of help, just add `-h` to see all the possibile options

### Data pre-processing

The pre-processing uses data in `data/` folder to create pickle files in `pkl` folder ready for the training. To pre-process data, you can:
- Create your own setting confifuration in `preprocess/setting/`, e.g. `preprocess/setting/mysetup.json`. Follow the structure of `default.json` in case of troubles.
- Use the following command to store your pre-processed data in `mypkl` output folder:
```
./preprocess_data -l mypkl -s mysetup
```
### Training model

The pre-processed data in a given folder, labeled e.g. `pkl/v1` is used to train a model that is specified in input, e.g. `mymodel` that is defined in `training/models/mymodel.py` (use the available files in the folder as examples to deveolp yours). This is then saved in pkl file (models and data used for the training):

```
./train_model -d -m mymodel -v myvalidation -l mylabel
```

### Test model
The trained model with the corresponding sets are read in order to make the analysis and evaluate the performance on test/train sets. The analysis, e.g.`myanalysis.py` to conduct is in `testing/myanalysis.py`. Since the reading is standard, only the `execute` function must be changed.

```
./test_model -d -a simple -i pkl/v1/model/mylabel
```


And enjoy!

## FAQ

### Why the prepare_data is not working?
You probably need a `dataprep/conf.py` that includes the connection to database of FW. Since this is private, use the dataset available in `data/` please.
