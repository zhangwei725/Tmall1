from django.conf.urls import url

from apps.cars import views

urlpatterns = [
    url('add/', views.add_car, name='add_car'),
    url('show/', views.show, name='show'),
    url('edit/', views.edit, name='edit'),
    url('delete/', views.delete, name='delete'),
]
