from django.urls import path
from user.views import *
urlpatterns = [

    path('default/',default_page,name='default_page'),
    path('user_login/',user_login,name='user_login'),
    path('user_register/',user_register,name='user_register'),
    path('user_verification/',user_verification,name='user_verification'),
    path('login/',login_view,name='login_view'),
    path('logout/',user_logout,name='user_logout'),
    path('get_current_user/',get_current_user,name='get_current_user'),
    path('update_user/',update_user,name='update_user'),
    path('search/',search_users,name='search_users'),
    path('get_by_username/',get_by_username,name='get_by_username'),
    path('verify_and_reset_password/',verify_and_reset_password,name='verify_and_reset_password'),
]