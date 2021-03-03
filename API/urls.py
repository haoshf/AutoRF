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

from . import views
urlpatterns = [
    re_path(r'run_xn$', views.run_xn),
    re_path(r'jmx_list$',views.jmx),
    re_path(r'up_jmx$', views.up_jmx),
    re_path(r'detail-(?P<page>\w+)',views.jmx_detail),
    re_path(r'xn_logs$', views.xn_logs),
    re_path(r'xn_download$', views.xn_download),
]
