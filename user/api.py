from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from lib.sms import send_sms
from lib.http import render_json

def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    phone = request.POST.get('phone')
    result,msg = send_sms(phone)

    return render_json(msg)



def submit_vcode(request):
    """通过验证码登录注册"""
    if not request.method == "POST":
        return HttpResponse('request method error')

    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    cache_vcode = cache.get()


def get_profile(request):
    """获取个人资料"""
    pass


def set_profile(request):
    """修改个人资料"""
    pass


def upload_avatar(request):
    """头像上传"""
    pass


