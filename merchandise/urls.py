from django.urls import path
from .views import merchandise_detail, merchandise_list_create, toggle_like, get_liked_merchandise, get_my_merchandise, \
    search_merchandise, merchandiseDetail

urlpatterns = [
    path('', merchandise_list_create, name='merchandise-list'),
    path('<int:merchandise_id>/', merchandise_detail, name='merchandise-detail'),
    path('<int:merchandise_id>/like/', toggle_like, name='toggle_like'),
    path('get-liked-merchandise/', get_liked_merchandise, name='liked_merchandise'),
    path('my-merchandise/',get_my_merchandise, name='my-merchandise'),
    path('search/',search_merchandise,name='search_merchandise'),
    path('merchandiseDetail/<int:merchandise_id>/', merchandiseDetail, name='merchandiseDetail'),
 # ✅ 新增 API
]
