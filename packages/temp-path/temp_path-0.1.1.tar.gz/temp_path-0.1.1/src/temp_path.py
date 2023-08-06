import sys
from contextlib import contextmanager


@contextmanager
def temp_path(path):
    """Temporarily add a folder to the path.

    Parameters
    ----------
    path : str, pathlib.Path
        The path to be added to the path.
    """
    path = str(path)
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)
