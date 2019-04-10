import os
from swiper import settings
from lib.qiniu_cloud import upload_to_qiniu
from swiper import config
from urllib.parse import urljoin
from worker import celery_app

def upload_avatar_to_server(uid, avatar):

    file_name = 'avatar-%s' % uid + os.path.splitext(avatar.name)[1]
    save_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, file_name)

    with open(save_path, 'wb') as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)

    return file_name, save_path

@celery_app.task
def upload_avatar(user, avatar):

    file_name, saved_path = upload_avatar_to_server(user.id, avatar)
    upload_to_qiniu(file_name, saved_path)
    avatar_url = urljoin(config.QINIU_BUCKET_URL,file_name)
    user.avatar = avatar_url
    user.save()