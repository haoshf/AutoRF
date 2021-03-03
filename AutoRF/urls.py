"""AutoRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import include
# from API.views import page_not_found
# from django.conf.urls import handler404, handler500
# from django.views import static
# from django.conf import settings

urlpatterns = [
    # re_path(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    re_path('admin/', admin.site.urls),
    re_path(r'^work', include('Work.urls')),
    re_path(r'^api', include('API.urls')),
    re_path(r'', include('backend.urls')),
]

#找不到时返回首页
# handler404 = "API.views.page_not_found"
