import datetime
from user.models import User
from social.models import Swipe


def get_rcmd_users(user):

    current_year = datetime.date.today().year
    max_dating_year = current_year - user.profile.min_dating_age
    min_dating_year = current_year - user.profile.max_dating_age

    #已经滑动过的用户id
    swiped = Swipe.objects.filter(uid=user.id).only('sid')
    swiped_uid_list = [swipe.id for swipe in swiped]
    swiped_uid_list.append(user.id) #排除自己

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__range=[min_dating_year,max_dating_year],
    ).exclude(id__in=swiped_uid_list)[0:20]

    return users