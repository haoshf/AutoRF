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
    re_path(r'task.html$',views.task),
    re_path(r'run_project.html$', views.run_project),
    re_path(r'run_suite.html$', views.run_suite),
    re_path(r'rerun.html$', views.rerun),
    re_path(r'check_status.html$', views.check_start),
    re_path(r'mt_check.html$', views.mt_check),
    re_path(r'stop.html$', views.stop_process),
    re_path(r'task_del.html$', views.del_task),
    re_path(r'trigger.html$', views.trigger_list),
    re_path(r'get_trigger$', views.get_trigger),
    re_path(r'trigger_update$', views.trigger_update),
    re_path(r'trigger_start-(\d+)$', views.trigger_start),
    re_path(r'trigger_stop-(\d+)$', views.trigger_stop),
]
