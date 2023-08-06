from collections import Mapping


def deep_iterator(d : Mapping):
    def _deep_iterator(d : Mapping, path : tuple):
        for k, v in d.items():
            if isinstance(v, Mapping):
                yield from _deep_iterator(v, (*path, k))
            else:
                yield (*path, k), v
    yield from _deep_iterator(d, ())
