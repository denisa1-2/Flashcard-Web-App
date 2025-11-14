from django.urls import path
from .import views

urlpatterns = [
    path('create/',views.create_set, name='create_set'),
    path('read/',views.read_sets, name='read_sets'),
    path('', views.home, name='home'),
    path('predefinde/', views.predefined_list, name='predefined_list'),
    path('predefined/<str:set_key>/', views.predefined_set, name='predefined_set'),
]