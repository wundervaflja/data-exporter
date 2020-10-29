import datetime
from typing import List


class BitbucketCommitInfo:
    repo_name: str
    hash: str
    author_uuid: str = None
    author_account_id: str = None
    message: str = None
    date: datetime.datetime = None
    type: str = None
    parents: List[str] = None
    lines_added: int = None
    lines_removed: int = None


def get_commit_payload(repo_name, commit, commit_stats):
    commit_info = BitbucketCommitInfo()
    commit_info.repo_name = repo_name
    commit_info.hash = commit.get("hash")
    author = commit.get("author") or {}
    user = author.get("user") or {}
    commit_info.author_uuid = user.get("uuid")
    commit_info.author_account_id = user.get("account_id")
    commit_info.message = commit.get("message")
    commit_info.date = commit.get("date")
    commit_info.type = commit.get("type")
    parents = []
    for parent in commit.get("parents"):
        parents.append(parent.get("hash"))
    commit_info.parents = parents
    commit_info.lines_added, commit_info.lines_removed = commit_stats
    return commit_info
