import xadmin
from xadmin import views

# 主题的修改
class BaseSystemSettings:
    # 开启修改主题
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSystemSettings)


class GlobalSettings:
    site_title = '天猫后台管理系统'
    site_footer = '阿里巴巴科技有限公司'


# 注册
xadmin.site.register(views.CommAdminView, GlobalSettings)


# class TestAdmin:
#     # 后台管理界面显示的列
#     list_display = ['tid', 'name', ]
#     # 搜索的列名
#     search_fields = ['name']
#     # 分页显示的条数
#     list_per_page = 10
#     ordering = ['-tid']
#     # 不允许编辑
#     # readonly_fields = ['name']


# xadmin.site.register(PropertyValue)
# xadmin.site.register(Property)
# xadmin.site.register(Review)
# xadmin.site.register(SubMenu)
# xadmin.site.register(SubMenu2)
# xadmin.site.register(Category)
# xadmin.site.register(Shop)
# xadmin.site.register(ShopImage)
# xadmin.site.register(ShopCar)
