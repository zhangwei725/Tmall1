from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.shop.models import Shop
from apps.home.models import BaseModel


class User(AbstractUser):
    phone = models.CharField(max_length=11, default='110')
    desc = models.CharField(max_length=255, null=True)
    uid = models.AutoField('用户ID', primary_key=True)
    icon = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='upload/img/%Y%m%d',
                             default=u"apps/static/img/default.png")

    class Meta:
        db_table = 'user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    # def img_show(self):
    #     """
    #     后台显示图片
    #     :return:
    #     """
    #     return u'<img width=50px src="%s" />' % self.icon.url
    #
    # img_show.short_description = '头像'
    # # 允许显示HTML tag
    # img_show.allow_tags = True


class Review(BaseModel):
    review_id = models.AutoField('ID', primary_key=True)
    content = models.CharField('内容', max_length=4000, )
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, db_index=True, verbose_name="商品ID")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='uid', db_index=True,
                             verbose_name='用户ID')

    class Meta:
        db_table = 'review'
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class Address(BaseModel):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.CharField(max_length=6, null=True)
    is_default = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    county = models.CharField(max_length=64)

    class Meta:
        db_table = 'address'
        ordering = ['address_id']
