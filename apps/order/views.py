import datetime
import random
from decimal import Decimal
from time import timezone

from django.db import transaction
from django.shortcuts import render, redirect

# django 如何获取多个值    getlist('key')
from django_redis import get_redis_connection

from apps.cars.models import ShopCar
from apps.order.models import OrderInfo, Order


def confirm_order(request):
    # 获取用户选中的记录
    checks = request.POST.getlist('ck')  # ['0','1']
    if checks:
        check_dict = {}
        id_list = []
        numbers = request.POST.getlist('number')  # ['10','1'...]
        ids = request.POST.getlist('car_id')
        for index in checks:
            # check_list.append()
            # id_list.append()
            # 字典如果想值作为key就必须采用[key]方式
            check_dict[ids[int(index)]] = numbers[int(index)]
            # key = check_dict[ids[include(include)]]
            # value = numbers[int(include)]
            # check_dict.update(key=value)
        try:
            with transaction.atomic():
                # 保存 确认购买的商品的数量
                for key, value in check_dict.items():
                    ShopCar.objects.filter(car_id=int(key)).update(number=int(value), status=2)

        except:
            pass

    # 如果该条购车记录被选中  更新数据库的数量
    cars = ShopCar.objects.filter(user_id=request.user.userprofile.uid, status=2)
    if cars:
        for car in cars:
            # 获取 商品的图片信息
            car.img = car.shop.shopimage_set.all().first()
    return render(request, 'test/confirm.html', {'cars': cars})


# 使用时间  + 随机数
# 事务 一系列增改该的操作
# 1> 开启事务
# 2> 多个增删改
# 3> 提交事务 或回滚

"""
django 事务的常用的两种方式
1  装饰器
 @transaction.atomic  
    作用整个视图函数  
    注意: 不能再视图函数里处理异常
2  使用with 语法
    try 
        with  transaction.atomic():
#            多个sql操作
    :except
        pass
"""


# django  默认开启
def create_order(request):
    address = request.POST.get('address')
    pay_code = request.POST.getlist('rd')
    # 生成订单号
    try:
        with transaction.atomic():
            uid = request.user.userprofile.uid
            order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 10))
            order = Order(order_code=order_code,
                          address='湖北武汉市高新区金融港', receiver='小玲',
                          user_message='请送货的时候给我带包辣条',
                          mobile='110',
                          user_id=uid)
            order.save()
            #  用户下面购物车的数据清空
            # 1 表示正常  0表示删除
            ShopCar.objects.filter(user_id=uid, status=1).update(status=-1, order=order)
        if pay_code == 1:
            pass
            # 微信支付
        else:
            # 支付宝支付
            pass
    except:
        pass


def create(self, validated_data):
    """创建订单记录：保存OrderInfo和OrderGoods信息"""
    # 获取当前保存订单时需要的信息
    # 获取当前的登录用户
    user = self.context['request'].user
    # 生成订单编号
    order_id = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
    # 获取地址和支付方式
    address = validated_data.get('address')
    pay_method = validated_data.get('pay_method')
    # 开启事务
    with transaction.atomic():
        # 在安全的地方，创建保存点，将来操作数据库失败回滚到此
        save_id = transaction.savepoint()
        try:
            # 保存订单基本信息 OrderInfo
            order = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address,
                total_count=0,
                total_amount=0,
                freight=Decimal('10.00'),
                pay_method=pay_method,
                # 如果用户传入的是"支付宝支付"，那么下了订单后，订单的状态要是"待支付"
                # 如果用户传入的是"货到付款"，那么下了订单后，订单的状态要是"代发货"
                status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']
                if pay_method ==OrderInfo.PAY_METHODS_ENUM['ALIPAY']
                else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
            )
            # 从redis读取购物车中被勾选的商品信息
            redis_conn = get_redis_connection('carts')
            # 读取出所有的购物车数据
            # redis_cart = {b'1':b'10', b'2':b'20', b'3':b'30'}
            redis_cart = redis_conn.hgetall('cart_ % s' % user.id)
            # cart_selected = [b'1', b'2']
            cart_selected = redis_conn.smembers('selected_ % s' % user.id)
            # 定义将来要支付的商品信息的字典
            # carts = {1:10, 2:20}
            carts = {}
            for sku_id in cart_selected:
                carts[int(sku_id)] = int(redis_cart[sku_id])
            # 读取出所有要支付的商品的sku_id
            # sku_ids = [1,2]
            sku_ids = carts.keys()
            # 遍历购物车中被勾选的商品信息
            for sku_id in sku_ids:
                # 死循环的下单：当库存满足，你在下单时，库存没有同时的被别人的更改，下单成功
                # 如果下单库存被更改，但是你的sku_count依然在被更改后的库存范围内，继续下单
                # 直到库存真的不满足条件时才下单失败
                while True:
                    # 获取sku对象
                    sku = SKU.objects.get(id=sku_id)
                    # 获取原始的库存和销量
                    origin_stock = sku.stock
                    origin_sales = sku.sales
                    sku_count = carts[sku_id]
                    # 判断库存?
                    if sku_count > origin_stock:
                        # 回滚
                        transaction.savepoint_rollback(save_id)
                        raise serializers.ValidationError('库存不足')
                        # 读取要更新的库存和销量
                        new_stock = origin_stock - sku_count
                        new_sales = origin_sales + sku_count
                        # 使用乐观锁更新库存:在调用update()去更新库存之前，使用filter()拿着原始的库存去查询记录是否存在
                        # 如果记录不存在的，在调用update()时返回0
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        if 0 == result:
                            # 死循环的下单：当库存满足，你在下单时，库存没有同时的被别人的更改，下单成功
                            # 如果下单库存被更改看，但是你的sku_count依然在被更改后的库存范围内，继续下单
                            # 直到库存真的不满足条件时才下单失败
                            continue
                        # 修改SPU销量
                        sku.goods.sales += sku_count
                        sku.goods.save()
                        # 保存订单商品信息 OrderGoods
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price,
                        )
                        # 累加计算总数量和总价
                        order.total_count += sku_count
                        order.total_amount += (sku_count * sku.price)
                        # 下单成功要跳出死循环
                        break
                # 最后加入邮费和保存订单信息
                order.total_amount += order.freight
                order.save()
        except Exception:
            transaction.savepoint_rollback(save_id)
            raise  # 自动的将捕获的异常抛出，不需要给异常起别名
        # 没有问题，需要明显的提交
        transaction.savepoint_commit(save_id)
        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('cart_%s' % user.id, *sku_ids)
        pl.srem('selected_ % s' % user.id, *sku_ids)
        pl.execute()
        # 响应结果
    return order
