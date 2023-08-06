import json
import os
from datetime import datetime
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import frontmatter
import tablib
from jinja2.sandbox import SandboxedEnvironment
from tablib.formats._json import date_handler

# Walking the query_files dir to get all the queries in a single list
# NOTE: this means query names should be unique across subdirectories,
#       *and* adding a new query file requires restart
FLAT_QUERIES = list(Path(os.getenv('QUERY_PATH', 'query_files')).glob('**/*'))


def get_query(query_name):
    """Find file matching query_name, read and return query object
    """
    query_file_match = list(
        filter(lambda i: query_name == i.stem, FLAT_QUERIES))
    if not query_file_match:
        return None
    # TODO: Log warning if more than one match
    query_file = query_file_match[0]
    with open(query_file) as f:
        metadata, query_body = frontmatter.parse(f.read())
    result_mod = query_file.suffix.strip('.')
    query_obj = SimpleNamespace(
        name=query_name,
        metadata=metadata,
        path=query_file,
        result_mod=result_mod,
        body=query_body,
        error=False,
        executed=datetime.utcnow().isoformat())
    return query_obj


def process_template(sql, **kwargs):
    env = SandboxedEnvironment()
    template = env.from_string(sql)
    return template.render(kwargs)


# TODO: try this in python console
def get_result_set(query_name, **kwargs):
    """ Call get_query, then submit query from file to resultset module
    """
    query = get_query(query_name)
    if not query:
        query = SimpleNamespace()
        query.error = f"No query found matching '{query_name}'"
        return query
    try:
        result_mod = import_module(
            f'nerium.contrib.resultset.{query.result_mod}')
    except ModuleNotFoundError:
        result_mod = import_module('nerium.resultset.sql')
    query.params = {**kwargs}
    query.body = process_template(sql=query.body, **query.params)
    result = result_mod.result(query, **query.params)
    # Dumping and reloading via json here gets us datetime and decimal
    # serialization handling courtesy of `tablib`
    query.result = json.loads(json.dumps(result, default=date_handler))
    try:
        if 'error' in query.result[0].keys():
            query.error = query.result[0]['error']
    except IndexError:
        pass
    return query


def results_to_csv(query_name, **kwargs):
    """ Generate CSV from result data
    """
    query = get_result_set(query_name, **kwargs)
    result = query.result
    columns = list(result[0].keys())
    data = [tuple(row.values()) for row in result]
    frame = tablib.Dataset()
    frame.headers = columns
    for row in data:
        frame.append(row)
    csvs = frame.export('csv')
    return csvs
