import datetime


class RepositoryInfo:
    name: str
    mainbranch_name: str
    description: str


def get_repository_info(repository):
    repository_info = RepositoryInfo()
    repository_info.name = repository.git_dir.split('/')[-2]
    repository_info.mainbranch_name = repository.active_branch.name
    repository_info.description = repository.description
    return repository_info
