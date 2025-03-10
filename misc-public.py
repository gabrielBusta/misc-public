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


def schedule(tasks):
    print('#!/bin/bash\n')
    for t in tasks:
        print(f'# rerun {t}')
        print(f"echo \"scheduling {t}\"\n")
        print(f"taskcluster api queue scheduleTask \"{t}\"\n")


def load_task_graph(path):
    import json
    with open(path) as f:
        data = f.read()
    task_graph = json.loads(data)
    return task_graph


def load_firefox_ci_task_graph(task_id, task_run=0):
    import requests
    url = f"https://firefoxci.taskcluster-artifacts.net/{task_id}/{task_run}/public/task-graph.json"
    response = requests.get(url)
    task_graph = response.json()
    url = f"https://firefoxci.taskcluster-artifacts.net/{task_id}/{task_run}/public/label-to-taskid.json"
    response = requests.get(url)
    label_to_task_id = response.json()
    return task_graph, label_to_task_id


def rerun_failed_tasks_in_task_group(task_group_id, dry_run=True):
    import taskcluster
    from pprint import pp

    auth = taskcluster.Auth(taskcluster.optionsFromEnvironment())
    queue = taskcluster.Queue(auth.options)
    task_group = queue.listTaskGroup(task_group_id)
    failed_tasks_in_task_group = [
        task for task in task_group["tasks"] if task["status"]["state"] == "failed"
    ]
    print(f"Found {len(failed_tasks_in_task_group)} failed tasks in {task_group_id}.")
    failed_tasks_in_task_group_names = {
        task["task"]["metadata"]["name"]: task["status"]["taskId"]
        for task in failed_tasks_in_task_group
    }
    pp(failed_tasks_in_task_group_names)
    if dry_run:
        print("THIS IS A DRY RUN!")
    for task_name, task_id in failed_tasks_in_task_group_names.items():
        print(f"Rerunning {task_name} ({task_id})")
        if dry_run:
            print(f'Calling queue.rerunTask("{task_id}")')
        else:
            response = queue.rerunTask(task_id)
            run_id = response["status"]["runs"][-1]["runId"]
            run_state = response["status"]["runs"][-1]["state"]
            print(f"Run {run_id} for {task_name} is {run_state}.")
    print(f'DONE SUBMITTING FAILED TASK RERUNS FOR "{task_group_id}"')


def open_task(task_id):
    import webbrowser
    webbrowser.open(f"https://firefox-ci-tc.services.mozilla.com/tasks/{task_id}", new=2)


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
