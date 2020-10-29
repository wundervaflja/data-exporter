import datetime


class BitbucketRepositoryInfo:
    scm: str
    website: str
    has_wiki: bool
    name: str
    fork_policy: str
    uuid: str
    language: str
    created_on: datetime.datetime
    mainbranch_type: str
    mainbranch_name: str
    full_name: str
    has_issues: bool
    owner_uuid: str
    owner_account_id: str
    updated_on: datetime.datetime
    size: int
    type: str
    slug: str
    is_private: bool
    description: str


def get_repository_info(repository):
    repository_info = BitbucketRepositoryInfo()
    repository_info.scm = repository.get("scm")
    repository_info.website = repository.get("website")
    repository_info.has_wiki = repository.get("has_wiki")
    repository_info.name = repository.get("name")
    repository_info.fork_policy = repository.get("fork_policy")
    repository_info.uuid = repository.get("uuid")
    repository_info.language = repository.get("language")
    repository_info.created_on = repository.get("created_on")
    repository_info.mainbranch_type = repository.get("mainbranch").get("type")
    repository_info.mainbranch_name = repository.get("mainbranch").get("name")
    repository_info.full_name = repository.get("full_name")
    repository_info.has_issues = repository.get("has_issues")
    repository_info.owner_uuid = repository.get("owner").get("uuid")
    repository_info.owner_account_id = repository.get("owner").get("account_id")
    repository_info.updated_on = repository.get("updated_on")
    repository_info.size = repository.get("size")
    repository_info.type = repository.get("type")
    repository_info.slug = repository.get("slug")
    repository_info.is_private = repository.get("is_private")
    repository_info.description = repository.get("description")
    return repository_info
