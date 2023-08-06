# -*- coding: utf8 -*-


def get_keys(d):
    if isinstance(d, dict):
        return sorted(d.keys())

    if not d:
        return []

    return sorted(d[0].keys())


def dict_to_csv(d, fields):
    def get_row():
        for key in total_keys:
            yield obj.get(key, '')

    def get_obj():
        try:
            return next(items_iter)
        except StopIteration:
            return None

    if isinstance(d, dict):
        d = [d]

    total_keys = fields

    items_iter = iter(d)

    obj = get_obj() or {}

    if total_keys is None:
        total_keys = get_keys([obj])

    yield total_keys

    while True:
        yield list(get_row())
        obj = get_obj()
        if obj is None:
            break


def format_json_data(json_data, formatters=None):
    if formatters is None:
        return json_data

    for row in json_data:
        for field, formatter in formatters.items():
            if field in row:
                row[field] = formatter(row[field])

    return json_data
