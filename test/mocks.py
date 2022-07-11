
def mock_index_return(*args):
    """Used to mock find_index_by_key_value in unit tests and some integration tests
    works with the fake db in data.py"""
    if args[0] == "name" and (args[1] == "foo" or args[1] == "bar"):
        return 0
    if args[0] == "name" and args[1] == "fuu":
        return 1
    return -1
