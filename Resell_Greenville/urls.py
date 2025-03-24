"""
URL configuration for Resell_Greenville project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render,redirect
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.decorators import api_view

import user

@api_view(['POST',"GET"])
def csrf(request):
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('merchandise/',include('merchandise.urls')),
    path('csrf/',csrf,name='get_csrf_token'),
    path('messages/',include('message.urls')),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


