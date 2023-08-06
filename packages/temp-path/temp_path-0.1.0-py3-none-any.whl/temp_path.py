import sys
from contextlib import contextmanager


@contextmanager
def temp_path(path):
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)
