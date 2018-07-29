import os
import time

from django.core.files.storage import FileSystemStorage
from django.db import models


# --fake 是不执行该迁移脚本但是标记该脚本已经被执行过

class ImageStorage(FileSystemStorage):
    IMG_PREFIX = 'IMG_'
    FILE_TIME = time.strftime('%Y%m%d%H%M%S')
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super().__init__(location, base_url)
        # 重写 _save方法

    def _save(self, name, content):
        # 文件扩展名
        ext_name = name[name.rfind('.'):]
        # 文件目录
        image_path = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        image_name = self.IMG_PREFIX + self.FILE_TIME + ext_name
        image_file = os.path.join(image_path, image_name)
        # 调用父类方法
        return super()._save(image_file, content)


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Navigation(BaseModel):
    nav_id = models.AutoField(primary_key=True)
    nav_name = models.CharField(max_length=64)

    class Meta:
        db_table = 'navigation'
        verbose_name = '导航条'
        verbose_name_plural = verbose_name


class Banner(BaseModel):
    banner_id = models.AutoField('ID', primary_key=True)
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m%d', storage=ImageStorage(), max_length=100)
    detail_url = models.URLField('访问地址', max_length=200)
    order = models.IntegerField('顺序', default=1)
    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
