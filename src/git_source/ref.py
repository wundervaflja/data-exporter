import datetime


class RefInfo:
    repo_name: str
    name: str
    path: str
    target_hash: str
    tracking_branch: str


def get_ref_info(ref):
    ref_info = RefInfo()
    ref_info.repo_name = ref.repo.git_dir.split('/')[-2]
    ref_info.name = ref.name
    ref_info.path = ref.path
    if not ref.name.endswith('stash'):
        ref_info.tracking_branch = ref.tracking_branch().name if ref.tracking_branch() else ''
    else:
        ref_info.tracking_branch = ''
    ref_info.target_hash = ref.commit.hexsha
    return ref_info
