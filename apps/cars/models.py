from django.db import models

from apps.account.models import User
from apps.shop.models import Shop
from apps.order.models import Order


class ShopCar(models.Model):
    car_id = models.AutoField(verbose_name='ID', primary_key=True)
    number = models.IntegerField(verbose_name='商品数量', default=0)
    shop = models.ForeignKey(Shop, models.DO_NOTHING, verbose_name='商品ID')
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='uid', verbose_name='用户ID')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, db_column='oid', null=True, verbose_name='商品ID')
    # 1正常 -1 删除 ， 禁止 2
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'shop_car'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name



