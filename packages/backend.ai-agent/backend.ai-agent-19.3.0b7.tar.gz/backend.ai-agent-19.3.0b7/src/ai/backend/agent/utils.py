from typing import MutableMapping, Sequence


def update_nested_dict(dest, additions):
    for k, v in additions.items():
        if k not in dest:
            dest[k] = v
        else:
            if isinstance(dest[k], MutableMapping):
                assert isinstance(v, MutableMapping)
                update_nested_dict(dest[k], v)
            elif isinstance(dest[k], Sequence):
                assert isinstance(v, Sequence)
                dest[k].extend(v)
            else:
                dest[k] = v
