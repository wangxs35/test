from django.http import HttpResponse
from django.shortcuts import render

from lib.https import render_json
from social import logics


def get_rcmd_user(request):

    user = request.user
    users = logics.get_rcmd_users(user)
    users_list = [user.to_string() for user in users]

    return render_json(users_list)


def like(request):

    if not request.method == "POST":
        return HttpResponse('request method error')

    sid = request.POST.get('sid')
    mathed = logics.like(request.user,sid)

    return render_json({'mathed':mathed})


def superlike(request):
    pass


def dislike(request):
    pass


def regret(request):
    pass


def get_friends(request):
    pass


def get_friend_info(request):
    pass
