import functools
import time

import simplejson as simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

from apps.cars.models import ShopCar


def ajax_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return function(request, *args, **kwargs)
        json = simplejson.dumps({'status': -2, 'msg': 'not_authenticated'})
        return HttpResponse(json, mimetype='application/json')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
        return result

    return timed


@ajax_login_required
def add(request):
    result = {'status': 1, 'msg': 'success'}
    try:
        uid = request.user.id
        num = int(request.GET.get('num'))
        shop_id = int(request.GET.get('shop_id'))
        # 验证参数是否正确
        if shop_id and num and uid:
            count = request.session.get('count', 0) + 1
            # 先判断 该用户 购物车中 是否 存在 该商品
            cars = ShopCar.objects.filter(user=request.user, shop_id=shop_id)
            if cars:
                car = cars.first()
                # 如果存在，则仅作数量上的 加法
                car.number += num
                car.save(update_fields=['number'])
            else:
                # 不存在就添加商品
                car = ShopCar(user_id=uid, shop_id=shop_id, number=num)
                car.save()
                request.session['count'] = count
            result.update(count=count)
            return JsonResponse(result)
    except Exception as e:
        result = {'status': -1, 'msg': 'error'}
    return JsonResponse(result)


# 商品的图片  商品的名称  商品的价格   商品的数量
# values
@login_required
def show(request):
    cars = ShopCar.objects.filter(user_id=request.user.id, is_active=1)
    if cars:
        for car in cars:
            # 获取 商品的图片信息
            car.img = car.shop.image_set.all().first()
    return render(request, 'cars.html', {'cars': cars})


# 传入 cart id 和 count 改变Cart
@login_required
def edit(request, car_id, count):
    try:
        cart = ShopCar.objects.get(pk=int(car_id))
        cart.count = int(count)
        cart.save()
    except:
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})


@login_required
def delete(request, cid):
    try:
        cart = ShopCar.objects.get(pk=int(cid))
        cart.delete()
        data = {'ok': 1}
    except:
        data = {'ok': 0}
    return JsonResponse(data)
