def get_hash(filepath, hash_type="sha512"):
    """Function to return the digest hash of a file based on filename and algorithm"""
    import hashlib
    HASH_BLOCK_SIZE = 1024 * 1024
    digest = hashlib.new(hash_type)
    with open(filepath, "rb") as fobj:
        while True:
            chunk = fobj.read(HASH_BLOCK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def get_file_size(filepath):
    import os
    if not os.path.isfile(filepath):
        raise ValueError(f"The path '{filepath}' is not a valid file.")
    return os.path.getsize(filepath)


def load_taskgraph():
    import json
    f = open('./artifacts/task-graph.json')
    data = f.read()
    f.close()
    taskgraph = json.loads(data)
    return taskgraph


def load_firefox_ci_task_graph(task_id):
    import requests
    url = f"https://firefoxci.taskcluster-artifacts.net/{task_id}/0/public/task-graph.json"
    response = requests.get(url)
    task_graph = response.json()
    return task_graph


def pick(picks, d):
    from toolz import keyfilter
    return keyfilter(lambda k: k in picks, d)


def omit(omissions, d):
    from toolz import keyfilter
    return keyfilter(lambda k: k not in omissions, d)


def dict_from_json(json_string):
    import json
    return json.loads(json_string)


def data_from_filename(filename):
    with open(filename) as f:
        return f.read()


def pp(obj):
    from pprint import pprint as pp
    pp(obj)
