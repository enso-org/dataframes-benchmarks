# Enso Dataframes Benchmarks

A set of benchmarks that compares Enso's Table library performance against Python's Pandas.

To run the benchmarks you need Python 3 installed and available on your path, preferably that should be Python 3.6, but other versions may work as well.

You need the `pandas` library to be installed, the benchmarks require version `1.1.5`.
You can get it by running:

```
pip install pandas==1.1.5
```

Moreover you need a right version of enso engine distribution and a launcher.

To run the benchmarks just run `./run_benchmarks.py`. The script will download all data and run the benchmarks, saving results to `report/` directory.

The benchmarks were run on Ubuntu 18.04 and the automatic runner script uses `wget` to download the files, so it must be available on your PATH for it to work (or alternatively you can download the files manually as described in [`./data/README.md`](./data/README.md)).
Additionally you may want to install `tqdm` so that the benchmark runner can display a progress bar showing the estimate runtime, you can do so with `pip install tqdm`, however the script will also work without it - it will just not show the progressbar.

To process the results, you can use the `./report/Report.ipynb` notebook - it will load the data and create the relevant graphs. To use it you need Jupyter Notebook installed.
