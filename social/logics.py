import datetime
from user.models import User
from social.models import Swipe, Friend
from django.core.cache import cache
from common import keys
from swiper import config


def get_rcmd_users(user):

    current_year = datetime.date.today().year
    max_dating_year = current_year - user.profile.min_dating_age
    min_dating_year = current_year - user.profile.max_dating_age

    #已经滑动过的用户id
    swiped = Swipe.objects.filter(uid=user.id).only('sid')
    swiped_uid_list = [swipe.sid for swipe in swiped]
    swiped_uid_list.append(user.id) #排除自己

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__range=[min_dating_year,max_dating_year],
    ).exclude(id__in=swiped_uid_list)[0:20]

    return users


def like(user,sid):
    #滑动，创建一条滑动记录
    Swipe.swipe('like', user.id, sid)

    #查看对方是否喜欢过你
    if Swipe.is_someone_like_you(uid=sid, sid=user.id):
        Friend.make_friend(user.id, sid)
        return True
    else:
        return False

def superlike(user,sid):
    #滑动，创建一条滑动记录
    Swipe.swipe('superlike', user.id, sid)

    #查看对方是否喜欢过你
    if Swipe.is_someone_like_you(uid=sid, sid=user.id):
        Friend.make_friend(user.id, sid)
        """to_do: 消息推送到对方手机，你们匹配成功"""
        return True
    else:
        return False

def dislike(user,sid):
    Swipe.swipe('dislike', user.id, sid)


def regret(user):
    now = datetime.date.today()
    key = keys.REGRET_KEY % ( user.id, now)

    regret_times = cache.get(key, 0)
    now_time = datetime.datetime.now()

    if regret_times < config.REGRET_TIMES:
        regret_times += 1
        now_second = 86400 - now_time.hour * 3600 - now_time.minute * 60 - now_time.second
        cache.set(key, regret_times, now_second)

        record = Swipe.objects.filter(uid=user.id).latest('stime')
        #查询你们现在是否是好友，如果是，就解除好友

        Friend.break_up(uid1=user.id, uid2=record.sid)
        Friend.break_up(uid2=user.id, uid1=record.sid)

        record.delete()

        return True
    else:
        return False
