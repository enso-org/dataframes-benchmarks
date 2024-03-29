# Enso Dataframes Benchmarks

A set of benchmarks that compares Enso's Table library performance against
analogous operations in Python's Pandas.

The benchmarks are implemented in `src/Main.enso` and `python/baseline.py`
respectively. Related operations have analogous function names in both languages
and they were implemented using analogous constructs in both languages.

## Running the Benchmarks

To run the benchmarks you need:

- Python 3.7+ installed and available on your PATH as `python`.
- `pandas` version `1.1.5`,
- Enso engine and launcher, version `0.2.0`, built from commit
  `d2df28bc43fcfee614fb31780cd46a59ebb16127`, with launcher `enso` executable on
  your PATH,
- `wget` on your PATH if you want the script to download input data
  automatically.

You can use [`pyenv`](https://github.com/pyenv/pyenv) to manage python versions:

```
> pyenv install 3.7.9
```

> If you want to use this Python version for processing the results in Jupyter
> Notebook as described later, make sure that sqlite is properly set up. For
> example, on Ubuntu you may need to `apt install libsqlite3-dev` before
> installing Python.

To install `pandas` and additional dependencies that are useful for generating
the report, you can use [`poetry`](https://github.com/python-poetry/poetry/):

```
# Go to the root directory of the repository and type:
> poetry install
> poetry shell # to enter the shell that uses poetry's virtual environment
```

You can download just the launcher or the whole bundle for `0.2.0` from the
[`enso` repository](https://github.com/enso-org/enso/releases/tag/enso-0.2.0).
After extracting it, you need to add the launcher executable to your PATH. If
you downloaded just the launcher, make sure that the engine is installed by
running `enso install engine 0.2.0`.

After ensuring that all the dependencies are installed, you can run the
benchmarks with:

```
> ./run_benchmarks.py
```

If you are using `poetry`, make sure that you run the above command inside of
`poetry shell` or otherwise use:

```
poetry run ./run_benchmarks.py
```

The script will automatically download all input data and run the benchmarks,
saving results to `report/` directory. If you don't have `wget`, you can
manually download the input files as described in
[`./data/README.md`](./data/README.md).

## Processing the Results

The `./run_benchmarks.py` will generate files `enso_times.csv` and
`python_times.csv` that contain time measurements for each tested operation. To
generate plots comparing these measurements you can use a prepared Jupyter
Notebook at `./report/Report.ipynb`. It will load the data and create the
relevant graphs.

To use it, you need `jupyter` installed - it will be available if you have used
`poetry` for resolving benchmark dependencies as described above.

To prepare the report, first start Jupyter Notebook with:

```
> cd report/
> poetry run jupyter notebook
```

Then you can open the notebook `Report.ipynb` and select
`Kernel > Restart and Run All` to generate the report based on latest
measurements. The generated report can be exported with `File > Download As`.
