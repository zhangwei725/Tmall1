from django.db import models

# Create your models here.
from apps.category.models import Category
from apps.home.models import BaseModel


class Shop(models.Model):
    shop_id = models.IntegerField(verbose_name='商品ID', primary_key=True)
    name = models.CharField(verbose_name='商品名称', max_length=100)
    sub_title = models.CharField(verbose_name='商品标题', max_length=255)
    original_price = models.DecimalField(verbose_name='原价', max_digits=7, decimal_places=2)
    promote_price = models.DecimalField(verbose_name='折扣价', max_digits=7, decimal_places=2)
    stock = models.IntegerField(verbose_name='库存')
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True, verbose_name='商品分类')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop'
        verbose_name = '商品信息'
        verbose_name_plural = '商品管理'


class SKU(BaseModel):
    sku = models.OneToOneField(Shop, on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name='库存', default=0)
    sales = models.IntegerField(verbose_name='销量', default=0)

    class Meta:
        db_table = 'sku'


class Image(models.Model):
    img_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name='商品ID')
    type = models.CharField('图片类型', max_length=32, blank=True)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.img_id

    class Meta:
        db_table = 'image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class Property(models.Model):
    property_id = models.AutoField('商品属性', primary_key=True)
    name = models.CharField('属性名称', max_length=64)
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True, verbose_name="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'property'
        verbose_name = '商品属性'
        verbose_name_plural = verbose_name


class PropertyValue(models.Model):
    pro_value_id = models.IntegerField(verbose_name='ID', primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop_id', verbose_name="商品ID")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_column='property_id', verbose_name="属性ID")
    value = models.CharField('属性值', max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'property_value'
        verbose_name = '商品属性值'
        verbose_name_plural = verbose_name
