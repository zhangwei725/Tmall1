from django.conf.urls import url, include
import xadmin

from apps.home import views

urlpatterns = [
    # url('admin/', admin.site.urls),
    # 替换admin为xadmin
    url('xadmin/', xadmin.site.urls),
    url('^$', views.index, name='index'),
    url('home/', include('apps.home.urls')),
    url('account/', include('apps.account.urls')),
    url('cars/', include('apps.cars.urls')),
    url('search/', include('apps.search.urls')),
    url('order/', include('apps.order.urls')),
]
