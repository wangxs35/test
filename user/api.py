from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from common import keys, errors
from lib.sms import send_sms
from lib.https import render_json
from user import logics
from user.models import User
from user.forms import ProfileForm


def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    phone = request.POST.get('phone')
    result, msg = send_sms(phone)

    return render_json(msg)


def submit_vcode(request):
    """通过验证码登录注册"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    cache_vcode = cache.get(keys.VCODE_KEY % phone)

    if vcode == cache_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone, nickname=phone)
        request.session['uid'] = user.id
        return render_json(user.to_string())
    else:
        return render_json('verify code error', errors.VCODE_ERROR)


def get_profile(request):
    """获取个人资料"""
    uid = request.session.get('uid')
    user = User.ordering.get(id=uid)

    profile = user.profile

    return render_json(profile.to_string())


def set_profile(request):
    """修改个人资料"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    uid = request.session.get('uid')
    profile_form = ProfileForm(request.POST)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.id = uid
        profile.save()
        return render_json('modify profile success')

    else:
        raise render_json(profile_form.errors,errors.FROM_VALUE_ERROR)


def upload_avatar(request):
    """头像上传"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    avatar = request.FILES.get('avatar')
    uid = request.session.get('uid')
    user = User.objects.get(id=uid)

    logics.upload_avatar.delay(user, avatar)

    return render_json('upload success')
