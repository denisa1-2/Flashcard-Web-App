from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),

    path('create/',views.create_set, name='create_set'),
    path('read/',views.read_sets, name='read_sets'),

    path('set/<str:set_name>/', views.create_set, name='create_set'),
    path('seturi/set//edit/', views.edit_set, name='edit_set'),

    path('view/', views.view_set, name='view_set'),

    path('delete/', views.delete_set, name='delete_set'),

    path('predefinde/', views.predefined_list, name='predefined_list'),
    path('predefined/<str:set_key>/', views.predefined_set, name='predefined_set'),

]