import time
from typing import List


class CommitInfo:
    repo_name: str
    hash: str
    author_name: str = None
    author_email: str = None
    committer_name: str = None
    commiter_email: str = None
    message: str = None
    committed_date: float = None
    timezone: str = None
    parents: List[str] = None
    files: int = None
    lines: int = None
    deletions: int = None
    insertions: int = None


def get_commit_payload(commit):
    commit_info = CommitInfo()
    commit_info.repo_name = commit.repo.git_dir.split('/')[-2]
    commit_info.hash = commit.hexsha
    commit_info.author_name = commit.author.name
    commit_info.author_email = commit.author.email
    commit_info.committer_name = commit.committer.name
    commit_info.commiter_email = commit.committer.email
    commit_info.message = commit.message
    commit_info.committed_date = commit.committed_date
    commit_info.timezone = time.tzname
    parents = []
    for parent in commit.parents:
        parents.append(parent.hexsha)
    commit_info.parents = parents
    commit_info.files = commit.stats.total['files']
    commit_info.deletions = commit.stats.total['deletions']
    commit_info.insertions = commit.stats.total['insertions']
    commit_info.lines = commit.stats.total['lines']
    return commit_info
