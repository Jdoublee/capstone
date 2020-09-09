from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    userid = models.CharField(default=objects.name,
                              max_length=20,
                              null=True,
                              unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=20, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name


class Writing(models.Model):
    # 작성한사람이 없다
    objects = UserManager()
    title = models.CharField(max_length=100, verbose_name='기사 제목')
    writer = models.CharField(default=objects.name, max_length=20, null=True)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='작성일')
    scrap = models.IntegerField(default=0, verbose_name='스크랩 수')
    text = models.CharField(max_length=1000, verbose_name='기사 내용')
    category = models.CharField(default='', max_length=50, verbose_name='카테고리')
    photo = models.CharField(default='', max_length=500, verbose_name='사진 url')

    @property
    def scrap_update(self):
        self.scrap += 1
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class ScrapList(models.Model):
    objects = UserManager()
    user_info = models.CharField(default=objects.name,
                                 max_length=20,
                                 verbose_name='사용자 id')
    # user_scrap_id = models.IntegerField(default=0, verbose_name='스크랩 id')
    title = models.CharField(max_length=100, verbose_name='기사 제목')
    article_id = models.IntegerField(default=0, verbose_name='기사 번호')
    category = models.CharField(default='', max_length=50, verbose_name='카테고리')
    writer = models.CharField(default=objects.name, max_length=20, null=True)
    scrap_date = models.DateTimeField(default=timezone.now,
                                      verbose_name='스크랩 날짜')
    scrap = models.IntegerField(default=0, verbose_name='스크랩 수')

    def __str__(self):
        return self.title
