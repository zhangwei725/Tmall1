from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from apps.cars.models import ShopCar


@login_required
def add(request):
    try:
        uid = request.user.id
        num = int(request.GET.get('num'))
        shop_id = int(request.GET.get('shop_id'))
        # 验证参数是否正确
        if shop_id and num and uid:
            # 先判断 该用户 购物车中 是否 存在 该商品
            car = ShopCar.objects.get(user=request.user.userprofile, shop_id=shop_id)
            if car:
                # 如果存在，则仅作数量上的 加法
                car.number += num
                car.save(update_fields=['number'])
            else:
                # 不存在就添加商品
                car = ShopCar(user_id=uid, shop_id=shop_id, number=num)
                car.save()
                # 判断请求方式 是否是ajax，若是则返回json格式的 商品数量即可

            if request.is_ajax():
                count = ShopCar.objects.filter(user_id=uid).count()
                return JsonResponse({'count': count})
            else:
                return redirect('/cart')
        else:
            pass

    except Exception as e:
        return HttpResponse('error')


# 商品的图片  商品的名称  商品的价格   商品的数量
# values
@login_required
def show(request):
    cars = ShopCar.objects.filter(user_id=request.user.userprofile.uid, status=1)
    if cars:
        for car in cars:
            # 获取 商品的图片信息
            car.img = car.shop.shopimage_set.all().first()
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
