from django.core.cache import cache
from swiper.config import *
import requests
import random



#生成验证码
def generator_vcode(length=4):
    start = 10 ** (length - 1)
    end = 10 ** length
    return str(random.randrange(start, end))

#发送短信
def send_sms(phone_num):
    params = YZX_SMS_PARAMS.copy()
    vcode = generator_vcode()
    params['param'] = vcode
    params['mobile'] = phone_num

    cache.set()

    res = requests.post(url=YZX_SMS_URL, json=params)
    print(res.status_code)
    if res.status_code == 200:
        result = res.json()
        code = result.get('code')
        msg = result.get('msg')
        if code == '000000':
            return True,msg
        else:
            return False,msg
    else:
        return False,'server error'

if __name__ == '__main__':
    send_sms(18058766787)
