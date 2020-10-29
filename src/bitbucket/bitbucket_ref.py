import datetime


class BitbucketRefInfo:
    repo_name: str
    name: str
    default_merge_strategy: str
    type: str
    target_hash: str
    tagger_uuid: str
    tagger_account_id: str
    date: datetime.datetime
    message: str


def get_ref_info(ref, repo_name):
    ref_info = BitbucketRefInfo()
    ref_info.repo_name = repo_name
    ref_info.name = ref.get("name")
    ref_info.default_merge_strategy = ref.get("default_merge_strategy")
    ref_info.type = ref.get("type")
    ref_info.target_hash = ref.get("target").get("hash")
    tagger = ref.get("tagger") or {}
    tagger_user = tagger.get("user") or {}
    ref_info.tagger_uuid = tagger_user.get("uuid")
    ref_info.tagger_account_id = tagger_user.get("account_id")
    ref_info.date = ref.get("date")
    ref_info.message = ref.get("message")
    return ref_info
