import pandas as pd
CITATIONS_FILE = "../data/Parking_Citations_in_FY_2018.csv"
METERS_FILE = "../data/LADOT_Metered_Parking_Inventory___Policies.csv"

debug_mode = False

def print_debug(stmt):
    if debug_mode:
        print(stmt)

from time import perf_counter
def timed(name):
    def decorator(func):
        def wrapped(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter()
            diff_ms = (end-start)*1000.0
            if debug_mode:
                print(f"{name}: {diff_ms:.2f}ms")
            else:
                print(f"{diff_ms:.2f}")
            return result
        return wrapped
    return decorator

@timed("loading")
def load_files():
    citations = pd.read_csv(CITATIONS_FILE)
    meters = pd.read_csv(METERS_FILE)
    return (citations, meters)

@timed("fill_na")
def fillna(citations):
    # we can implement this by map (x -> if x == null then fill else x)
    citations["Meter Id"] = citations["Meter Id"].fillna("")

@timed("joining")
def join(citations, meters):
    meters = meters.set_index("SpaceID")
    joined = citations.join(meters, on="Meter Id")
    return joined

@timed("filter1")
def count_missing_meters(citations):
    isna = citations["Meter Id"].isna()
    missing = len(citations[isna])
    return missing

@timed("filter2")
def count_having_meters(joined):
    nonmissing = joined[joined["Meter Id"] != ""]
    return len(nonmissing)

@timed("map_and_filter1")
def count_broadway(joined):
    mask = joined["BlockFace"].fillna("").str.endswith("BROADWAY")
    filtered = joined[mask]
    return len(filtered)

@timed("map_and_filter2")
def filterMonday(joined):
    mask = pd.to_datetime(joined["Issue Date"]).dt.weekday == 0
    ticketsonMonday = len(joined[mask])
    return ticketsonMonday

if __name__ == "__main__":
    print_debug("Starting benchmarks")

    (citations, meters) = load_files()

    missing = count_missing_meters(citations)
    print_debug(missing)

    fillna(citations)

    joined = join(citations, meters)

    nonmissing = count_having_meters(joined)
    print_debug(nonmissing)

    broadway_tickets = count_broadway(joined)
    print_debug(broadway_tickets)

    #monday_tickets = filterMonday(joined)
    #print(monday_tickets)
