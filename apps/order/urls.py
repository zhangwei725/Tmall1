from django.conf.urls import url

from apps.order import views

urlpatterns = [
    url('confirm/', views.confirm_order, name='confirm'),
    url('create/', views.create_order, name='create'),
]
