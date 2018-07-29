from django.shortcuts import render

from apps.account.models import Review
from apps.home.models import Navigation, Banner

# 购物车
# 1> 登录
# 2> 添加
# 3> 查看购物车
from apps.category.models import *
from apps.cars.models import ShopCar
from apps.shop.models import Shop, Property, PropertyValue


def index(request):
    navigations = Navigation.objects.all()
    # 获取分类菜单的数据
    categories = Category.objects.all()
    for category in categories:
        category.subs = category.submenu_set.all()
        # 获取分类二级菜单的数据
        for sub in category.subs:
            # 获取分类二级菜单的子数据
            sub.subs2 = sub.submenu2_set.all()
        #    ======== 结束======
        # 获取分类的商品信息
        category.shops = category.shop_set.all()[0:5]
        # 获取商品的图片
        for shop in category.shops:
            shop.img = shop.shopimage_set.filter(type='type_single').order_by('shop_img_id').first()
    # 获取轮播图数据
    banners = Banner.objects.all().order_by('banner_id')
    if request.user.is_authenticated:
        count = ShopCar.objects.filter(user_id=request.user.userprofile.uid, status=1).count()
        request.session['count'] = count

    return render(request, 'index.html', {'navigations': navigations,
                                          'banners': banners,
                                          'categories': categories})


# 商品id   87  90
def shop_detail(request, id):
    try:
        shop = Shop.objects.get(shop_id=id)
        shop.imgs = shop.shopimage_set.all()
        count = Review.objects.filter(shop_id=id).count()

        # 先查询分类表
        # 在去查询产品属性表
        # 在去查询差评的属性值
        properties = Property.objects.filter(cate_id=shop.cate.cate_id)
        for property in properties:
            property.pro_value = PropertyValue.objects.get(shop_id=id, property_id=property.property_id)

        return render(request, 'shop_detail.html', {"shop": shop, 'count': count, 'properties': properties})

    except Shop.DoesNotExist as e:
        pass
    except Shop.MultipleObjectsReturned as e:
        pass
