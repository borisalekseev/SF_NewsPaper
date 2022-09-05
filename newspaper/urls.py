from django.contrib import admin
from django.urls import path, re_path, include
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('news/')
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    path('', redirect_view)
]
