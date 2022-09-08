# fanta-voto-ai
ML algorithm to estimate the vote for FantaWomen based on available data.

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
And enjoy!

## FAQ

### Why the prepare_data is not working?
You probably need a `dataprep/conf.py` that includes the connection to database of FW. Since this is private, use the dataset available in `data/` please.
