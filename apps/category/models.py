from django.db import models

from apps.home.models import BaseModel


class Category(BaseModel):
    cate_id = models.AutoField('分类ID', primary_key=True)
    name = models.CharField('名称', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '分类菜单'
        verbose_name_plural = verbose_name


class SubMenu(models.Model):
    sub_menu_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255, blank=True, null=True)
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True,
                             verbose_name='父菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_menu'
        verbose_name = '一级菜单'
        verbose_name_plural = verbose_name


class TwoMenu(BaseModel):
    sub_menu2_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255)
    sub_menu = models.ForeignKey(SubMenu, models.DO_NOTHING,
                                 verbose_name='一级菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'two_menu'
        verbose_name = '二级菜单'
        verbose_name_plural = verbose_name
