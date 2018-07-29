from django.shortcuts import render

from apps.account.models import Review
from apps.home.models import Navigation, Banner

# 购物车
# 1> 登录
# 2> 添加
# 3> 查看购物车
from apps.category.models import *
from apps.cars.models import ShopCar


def index(request):
    navigations = Navigation.objects.all()
    # 获取分类菜单的数据
    categories = Category.objects.all()
    for category in categories:
        category.subs = category.submenu_set.all()
        # 获取分类二级菜单的数据
        for sub in category.subs:
            # 获取分类二级菜单的子数据
            sub.subs2 = sub.twomenu_set.all()
        #    ======== 结束======
        # 获取分类的商品信息
        category.shops = category.shop_set.all()[0:5]
        # 获取商品的图片
        for shop in category.shops:
            shop.img = shop.image_set.filter(type='type_single').order_by('img_id').first()
    # 获取轮播图数据
    banners = Banner.objects.all().order_by('banner_id')
    if request.user.is_authenticated:
        count = ShopCar.objects.filter(user_id=request.user.id, status=1).count()
        request.session['count'] = count

    return render(request, 'index.html', {'navigations': navigations,
                                          'banners': banners,
                                          'categories': categories})


