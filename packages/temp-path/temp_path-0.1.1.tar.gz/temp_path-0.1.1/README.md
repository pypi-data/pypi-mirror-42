# temp_path

This is a package to allow you to add a folder to the path temporarily.

Often when you deal with other people's code, it's not set up to be importable /
packaged. This tool allows you to import from those files anyways, without
having to permanently modify your path.

Simply run:

```python
from temp_path import temp_path
with temp_path('../someone/elses/code'):
    import their.messy.code

their.messy.code.use()
```

Of course, this is not just for importing python modules but also for other
stuff you might need on your path.
