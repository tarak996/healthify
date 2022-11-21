from django.urls import path
from . import views

urlpatterns = [
    path('', views.base),
    path('home/', views.home),
    path('sign', views.sign, name='signup'),
    path('login/', views.logins, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('additem/', views.additem, name="additem"),
    path("details/<id>", views.details, name="details"),
    path('delete/<int:id>/', views.delete_date),
    path('delete', views.delete_item),


]