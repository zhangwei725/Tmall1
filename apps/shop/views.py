from django.shortcuts import render

from apps.account.models import Review
from apps.shop.models import Shop, Property, PropertyValue


def shop_detail(request, id):
    try:
        shop = Shop.objects.get(shop_id=id)
        shop.imgs = shop.image_set.all()
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
