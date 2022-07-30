import time
from test.data import db as data
from gudlft.filesystem import load_data, save_data


def test_save_time():
    start = time.time()
    save_data(data)
    end = time.time()
    print(f"\nDB Saving Time: {round(end - start, 6)} seconds < 0.1sec")
    assert round(end - start, 6) < 1


def test_load_time():
    start = time.time()
    load_data(path="./test/JSON/")
    end = time.time()
    print(f"\nDB Loading  Time: {round(end - start, 6)} seconds < 0.1sec")
    assert round(end - start, 6) < 1
