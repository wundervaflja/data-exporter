import datetime


class BitbucketPullRequestInfo:
    repository_name: str
    id: int
    description: str
    title: str
    close_source_branch: bool
    type: str
    destination_commit_hash: str
    destination_commit_type: str
    destination_branch_name: str
    created_on: datetime.datetime
    source_commit_hash: str
    source_commit_type: str
    source_branch_name: str
    comment_count: int
    state: str
    task_count: int
    reason: str
    updated_on: datetime.datetime
    author_uuid: str
    author_account_id: str
    merge_commit_hash: str
    closed_by_uuid: str
    closed_by_account_id: str


def get_pull_request_info(repository_name, pull_request):
    pr_info = BitbucketPullRequestInfo()
    pr_info.repository_name = repository_name
    pr_info.id = pull_request.get("id")
    pr_info.description = pull_request.get("description")
    pr_info.title = pull_request.get("title")
    pr_info.close_source_branch = pull_request.get("close_source_branch")
    pr_info.type = pull_request.get("type")
    pr_info.destination_commit_hash = pull_request.get("destination").get("commit").get("hash")
    pr_info.destination_commit_type = pull_request.get("destination").get("commit").get("type")
    pr_info.destination_branch_name = pull_request.get("destination").get("branch").get("name")
    pr_info.created_on = pull_request.get("created_on")
    source = pull_request.get("source") or {}
    source_commit = source.get("commit") or {}
    pr_info.source_commit_hash = source_commit.get("hash")
    pr_info.source_commit_type = source_commit.get("type")
    pr_info.source_branch_name = pull_request.get("source").get("branch").get("name")
    pr_info.comment_count = pull_request.get("comment_count")
    pr_info.state = pull_request.get("state")
    pr_info.task_count = pull_request.get("task_count")
    pr_info.reason = pull_request.get("reason")
    pr_info.updated_on = pull_request.get("updated_on")
    pr_info.author_uuid = pull_request.get("author").get("uuid")
    pr_info.author_account_id = pull_request.get("author").get("account_id")
    merge_commit = pull_request.get("merge_commit") or {}
    pr_info.merge_commit_hash = merge_commit.get("hash")
    closed_by = pull_request.get("closed_by") or {}
    pr_info.closed_by_uuid = closed_by.get("uuid")
    pr_info.closed_by_account_id = closed_by.get("account_id")
    return pr_info
