from qiniu import Auth, put_file, etag
from swiper import config

def upload_to_qiniu(key,localfile):


    # 构建鉴权对象
    q = Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)


    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(config.QINIU_BUCKET_NAME, key, 3600)

    ret, info = put_file(token, key, localfile)
    print(info)

    return ret, info

