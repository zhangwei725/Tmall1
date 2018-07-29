from django.db import models

# Create your models here.
from apps.account.models import User, Address
from apps.home.models import BaseModel
from apps.shop.models import Shop


class OrderInfo(BaseModel):
    """
    订单信息
    """
    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }

    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "支付宝"),
    )

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }

    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="下单用户")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="收获地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name="订单状态")

    class Meta:
        db_table = "tb_order_info"
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """
    订单商品
    """
    SCORE_CHOICES = (
        (0, '0分'),
        (1, '20分'),
        (2, '40分'),
        (3, '60分'),
        (4, '80分'),
        (5, '100分'),
    )
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单")
    sku = models.ForeignKey(Shop, on_delete=models.PROTECT, verbose_name="订单商品")
    count = models.IntegerField(default=1, verbose_name="数量")
    # max_digits ：最大的位数。decimal_places ：小数点后面保留多少位
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    comment = models.TextField(verbose_name="评价信息")
    score = models.SmallIntegerField(choices=SCORE_CHOICES, default=5, verbose_name='满意度评分')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    is_commented = models.BooleanField(default=False, verbose_name='是否评价了')

    class Meta:
        db_table = "tb_order_goods"
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class Order(models.Model):
    ORDER_STATUS = (
        (1, '正常'),
        (0, '异常'),
        (-1, '删除'),
    )

    oid = models.AutoField('订单ID', primary_key=True)
    # 订单号唯一
    order_code = models.CharField('订单号', max_length=255)
    user_message = models.CharField('附加信息', max_length=255)
    pay_date = models.DateTimeField('支付时间', max_length=0,
                                    blank=True, null=True)
    delivery_date = models.DateTimeField('交易日期', blank=True, null=True)
    confirm_date = models.DateTimeField('确认日期', blank=True, null=True)
    """ 1正常 0 异常, -1 删除 """
    status = models.IntegerField('订单状态', choices=ORDER_STATUS, default=1)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='uid', verbose_name="用户ID")

    def __str__(self):
        return self.order_code

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
