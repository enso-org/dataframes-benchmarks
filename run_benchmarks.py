#!/usr/bin/env python

import sys, os, subprocess

if sys.version_info[0] != 3:
    print("Python 3 is required for running the script.")
    sys.exit(1)

pandas_version = "1.1.5"

try:
    import pandas as pd
    if pd.__version__ != pandas_version:
        print(f"Pandas {pd.__version} is installed, but {pandas_version} is required.")
        sys.exit(1)
except ModuleNotFoundError:
    print(f"Pandas {pandas_version} is required.")
    sys.exit(1)

root_path = os.path.abspath(os.path.join(__file__, os.pardir))
cwd = os.path.abspath(os.getcwd())
if root_path != cwd:
    print("Please run the script from the root directory of the repo.")
    sys.exit(1)

citations = "./data/Parking_Citations_in_FY_2018.csv"
meters = "./data/LADOT_Metered_Parking_Inventory___Policies.csv"
citations_url = "https://data.lacity.org/api/views/nma9-y7yc/rows.csv?accessType=DOWNLOAD"
meters_url = "https://data.lacity.org/api/views/s49e-q6j2/rows.csv?accessType=DOWNLOAD"

files = [(citations, citations_url), (meters, meters_url)]

for (f, url) in files:
    if not os.path.exists(f):
        print(f"{f} is missing, it will be downloaded from {url}")
        res = subprocess.run(["wget", "-O", f, url])
        if res.returncode != 0:
            print("Download failed")
            sys.exit(1)
headers = [
    "loading",
    "filter1",
    "fill_na",
    "joining",
    "filter2",
    "map_and_filter1",
    # "map_and_filter2",
]

try:
    import tqdm
    wrap = tqdm.tqdm
except ModuleNotFoundError:
    def wrapper(arg):
        return arg
    wrap = wrapper

REPEATS = 20
print(f"Will run benchmarks {REPEATS} times.")

enso_report = "./report/enso_times.csv"
python_report = "./report/python_times.csv"

def write_line(f, entries):
    ensured_dots = list(map(lambda s: s.replace(",", "."), entries))
    f.write(",".join(ensured_dots) + "\n")
    f.flush()

def parse_output(stdout):
    return stdout.decode("utf-8").strip().split("\n")

with open(enso_report, "w") as enso_file:
    with open(python_report, "w") as python_file:
        write_line(enso_file, headers)
        write_line(python_file, headers)

        for i in wrap(range(1, REPEATS + 1)):
            print(f"Running Python - {i}")
            result = subprocess.run(["python", "baseline.py"], cwd="./python/", stdout=subprocess.PIPE)
            write_line(python_file, parse_output(result.stdout))

            print(f"Running Enso - {i}")
            result = subprocess.run(["enso", "run", "."], stdout=subprocess.PIPE)
            write_line(enso_file, parse_output(result.stdout))

print("Finished")
