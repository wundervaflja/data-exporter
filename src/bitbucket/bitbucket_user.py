import datetime


class BitbucketUserInfo:
    uuid: str
    display_name: str
    nickname: str
    created_on: datetime.datetime
    is_staff: bool
    account_status: str
    type: str
    account_id: str

def get_user_info(user):
    user_info = BitbucketUserInfo()
    user_info.uuid = user.get("uuid")
    user_info.display_name = user.get("display_name")
    user_info.nickname = user.get("nickname")
    user_info.created_on = user.get("created_on")
    user_info.is_staff = user.get("is_staff")
    user_info.account_status = user.get("account_status")
    user_info.type = user.get("type")
    user_info.account_id = user.get("account_id")
    return user_info
