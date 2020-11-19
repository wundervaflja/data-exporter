import json

from pybitbucket.auth import BasicAuthenticator
from pybitbucket.bitbucket import Client
from pybitbucket.commit import Commit
from pybitbucket.pullrequest import PullRequest
from pybitbucket.ref import Ref
from pybitbucket.repository import Repository
from pybitbucket.user import User
from requests import HTTPError
from ratelimit import limits, sleep_and_retry
import requests

from src.bitbucket.bitbucket_commit import get_commit_payload
from src.bitbucket.bitbucket_pull_request import get_pull_request_info
from src.bitbucket.bitbucket_ref import get_ref_info
from src.bitbucket.bitbucket_repository import get_repository_info
from src.bitbucket.bitbucket_user import get_user_info
from src.utils import get_logger, get_config

logger = get_logger("BitBucketAPI")
bitbucket_client = BasicAuthenticator(get_config("bitbucket.user_name"), get_config("bitbucket.app_password"), get_config("bitbucket.user_email"))
bitbucket_client = Client(bitbucket_client)
BATCH_SIZE = 100
ONE_HOUR_SEC = 3600

USER = {}

def add_remote_relationship_methods(self, data):
    for name, url in BitbucketBase.links_from(data):
        if (name not in [i.name for i in BitbucketSpecialAction]):
            setattr(self, name, partial(
                self.client.remote_relationship,
                template=url))

from pybitbucket.bitbucket import BitbucketBase, BitbucketSpecialAction
from functools import partial

BitbucketBase.add_remote_relationship_methods = add_remote_relationship_methods

def run(endpoint):

    repositories = get_config("bitbucket.repositories")
    host = get_config("azimu_api.host")
    port = get_config("azimu_api.port")
    url = f"{host}:{port}{endpoint}"
    for repository in repositories:
        process_repository(repository, url)
        # process_commits(repository, url)
        process_pull_requests(repository, url, "OPEN")
        process_pull_requests(repository, url, "MERGED")
        process_refs(repository, url)
        result = True
    return result


@sleep_and_retry
@limits(calls=350, period=ONE_HOUR_SEC)
def process_user(username, url):
    table_name = "bitbucket_user"
    user = None
    if username not in USER:
        try:
            user = User.find_user_by_username(username=username, client=bitbucket_client)
            logger.debug("BitBucket user - {}".format(user))
        except HTTPError:
            logger.debug("No BitBucket user - {}".format(username))
        if user:
            user_info = vars(get_user_info(user))
            r = requests.post(f'https://{url}/{table_name}',
                              json={"data": json.dumps(user_info, sort_keys=True, default=str)},
                              headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
            if r.status_code != 200:
                raise Exception(r.status_code)
            USER[username] = r.json()
            return r.json()
    else:
        return USER[username]


@sleep_and_retry
@limits(calls=100, period=ONE_HOUR_SEC)
def process_repository(repository, url):
    table_name = "bitbucket_repository"
    user_name = get_config("bitbucket.user_name")
    user_name, repo_name = repository.split("/")
    repository = Repository.find_repository_by_name_and_owner(repository_name=repo_name, owner=user_name, client=bitbucket_client)
    logger.debug("Bitbucket repository - {}".format(repository))
    repository_info = vars(get_repository_info(repository.data))
    logger.debug("BitBucket repository owner - {}".format(repository_info['owner_uuid']))
    process_user(repository_info['owner_uuid'], url)
    print(f'https://{url}/{table_name}')
    r = requests.post(f'https://{url}/{table_name}',
                      json={"repository": json.dumps(repository_info, sort_keys=True, default=str)},
                      headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
    if r.status_code != 200:
        raise Exception(r.status_code)
    return r.json()


# @sleep_and_retry
# @limits(calls=350, period=ONE_HOUR_SEC)
# def process_commits(repository, url):
#     table_name = "bitbucket_commit"
#     commits = []
#     user_name, repo_name = repository.split("/")
#     for commit in Commit.find_commits_in_repository(user_name, repo_name, client=bitbucket_client):
#         logger.debug("BitBucket commit - {}".format(commit))
#         commit_stats = get_commit_stats(repository, commit.hash)
#         commit_info = get_commit_payload(repository, commit.data, commit_stats)
#         process_user(commit_info.author_uuid, url)
#         commits.append(vars(commit_info))
#         if len(commits) == BATCH_SIZE:
#             r = requests.post(f'https://{url}/{table_name}', json={"repository": repository,
#                                                                   "data": json.dumps(commits, sort_keys=True,
#                                                                                      default=str)
#                                                                   },
#                               headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
#             if r.status_code != 200:
#                 print(r.raw)
#                 raise Exception(r.status_code)

#             commits = []
#     if commits:
#         r = requests.post(f'https://{url}/{table_name}', json={"repository": repository,
#                                                               "data": json.dumps(commits, sort_keys=True, default=str)
#                                                               },
#                           headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
#     return r.json()


# @sleep_and_retry
# @limits(calls=350, period=ONE_HOUR_SEC)
# def get_commit_stats(repo, commit_hash):
#     user_name, repository_name = repo.split("/")
#     url = "https://api.bitbucket.org/2.0/repositories/{username}/{repo_slug}/diffstat/{spec}"
#     r = bitbucket_client.session.get(
#         url.format(username=user_name, repo_slug=repository_name, spec=commit_hash))
#     total_lines_added = 0
#     total_lines_removed = 0
#     if r.status_code == 200:
#         response = r.json()
#         for file in response["values"]:
#             total_lines_added += file.get("lines_added")
#             total_lines_removed += file.get("lines_removed")
#     else:
#         logger.error("Bad response - {}".format(r.text))
#     logger.debug(f"Commit {commit_hash} stats - + {total_lines_added} and - {total_lines_removed}")
#     return total_lines_added, total_lines_removed


@sleep_and_retry
@limits(calls=150, period=ONE_HOUR_SEC)
def process_refs(repository, url):
    table_name = "bitbucket_ref"
    user_name, repository_name = repository.split("/")
    refs = Ref.find_refs_in_repository(user_name, repository_name, client=bitbucket_client)
    for ref in refs:
        logger.debug("Bitbucket ref - {}".format(ref))
        ref_info = vars(get_ref_info(ref.data, repository))
        if ref_info:
            r = requests.post(f'https://{url}/{table_name}',
                              json={"ref": json.dumps(ref_info, sort_keys=True, default=str),
                                    "repository": repository_name
                                    },
                              headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
            if r.status_code != 200:
                raise Exception(r.status_code)
        return r.json()


@sleep_and_retry
@limits(calls=150, period=ONE_HOUR_SEC)
def process_pull_requests(repository, url, state):
    table_name = "bitbucket_pull_request"
    user_name, repository_name = repository.split("/")
    pull_requests = PullRequest.find_pullrequests_for_repository_by_state(repository_name=repository_name,
                                                                          owner=user_name,
                                                                          client=bitbucket_client, state=state)
    for pr in pull_requests:
        try:
            logger.debug("BitBucket pull request - {}".format(pr.data))
            pr_info = vars(get_pull_request_info(repository, pr.data))
            process_user(pr_info['author_uuid'], url)
            r = requests.post(f'https://{url}/{table_name}',
                              json={"data": json.dumps(pr_info, sort_keys=True, default=str)},
                              headers={"AUTH_TOKEN": get_config("azimu_api.auth_token")})
            if r.status_code != 200:
                raise Exception(r.status_code)
            return r.json()
        except:
            logger.debug('Problem with {}'.format(pr))
