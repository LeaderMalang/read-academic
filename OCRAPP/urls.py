from django.urls import path
from.import views

urlpatterns = [
    path('',views.index, name='index'),
    path('form',views.form, name='form'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('app_admin/', views.app_admin, name='app_admin'),
]
