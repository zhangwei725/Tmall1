from django.conf.urls import url

from apps.shop import views

# 两种

# 动态路由   path/123/
# request  path/?shop_id=1
# request.GET.get('shop_id')

urlpatterns = [
    url('detail/(\d+)/', views.shop_detail, name='detail'),
]
