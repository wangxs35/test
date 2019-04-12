import datetime

from django.db import models
from lib.orm import ModelMixin
from django.utils.functional import cached_property

"""
id name age
1   fbb 30
2   fxg 40

user = User.object.get(id=1)

profile = Profile.object.get(id=user.id)


profile
id location dating_sex
1   hanghai male
2   beijing femal


"""

class User(models.Model, ModelMixin):

    SEX = (
        ('male', '男'),
        ('female', '女')
    )

    phonenum = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, unique=True, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=200,verbose_name='个人形象')
    location = models.CharField(max_length=20,verbose_name='常居地')


    @cached_property
    def age(self):
        today = datetime.date.today()
        birth_day = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        birth_timedelta = today - birth_day
        return birth_timedelta.days // 365

    @property
    def profile(self):

        if not hasattr(self, '_profile'): #查看自身有没有_profile属性，如果没有，就从数据库中查询
            profile, _ = Profile.objects.get_or_create(id=self.id)
            self._profile = profile

        return self._profile




class Profile(models.Model, ModelMixin):
    SEX = (
        ('male', '男'),
        ('female', '女')
    )

    location = models.CharField(max_length=20, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=8, choices=SEX, verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')


