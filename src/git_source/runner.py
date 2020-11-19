#! /usr/bin/env python

import os
import sys

import json
import requests

from git import Repo
from src.git_source.commit import get_commit_payload
from src.git_source.ref import get_ref_info
from src.git_source.repository import get_repository_info
from src.utils import get_logger, get_config


BATCH_SIZE = 100
ONE_HOUR_SEC = 3600


def run():
    host = get_config("azimu_api.host")
    port = get_config("azimu_api.port")
    path = get_config("azimu_repo_path")
    endpoint = "/data/git"
    url = f"{host}:{port}/{endpoint}"
    for repo in __get_repos(path):
        __process_repository(repo, url)
        __process_commits(repo, url)
        __process_refs(repo, url)

def __get_repos(path=''):
    path = os.path.abspath(path)
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            yield Repo(item_path)



def __process_repository(repo, url):
    table_name = 'git_repository'
    repo_info = vars(get_repository_info(repo))
    print(vars(repo_info))

    print(f'http://{url}/{table_name}')
    r = requests.post(f'http://{url}/{table_name}',
                      json={"repository": json.dumps(repo_info, sort_keys=True, default=str)},
                      headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})

    
def __process_commits(repo, url):
    table_name = 'git_commit'
    commits = []
    for commit in repo.iter_commits():
        commit_info = get_commit_payload(commit)
        commits.append(vars(commit_info))
        if len(commits) == BATCH_SIZE:
            r = requests.post(f'http://{url}/{table_name}',
                              json={"data": json.dumps(commits, sort_keys=True, default=str)},
                              headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
            if r.status_code != 200:
                print(r.raw)
                raise Exception(r.status_code)

            commits = []
    if commits:
        r = requests.post(f'http://{url}/{table_name}', 
                          json={"data": json.dumps(commits, sort_keys=True, default=str)},
                          headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
    return r.json()


def __process_refs(repo, url):
    table_name = 'git_ref'
    for ref in repo.refs:
        ref_info = vars(get_ref_info(ref))
        if ref_info:
            r = requests.post(f'http://{url}/{table_name}',
                              json={"ref": json.dumps(ref_info, sort_keys=True, default=str)},
                              headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
            if r.status_code != 200:
                raise Exception(r.status_code)
        return r.json()


if __name__ == '__main__':
    run()
