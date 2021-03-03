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

from .views import project,layout,resource,suite,testcase,keyword,library,runner,account
urlpatterns = [
    re_path(r'^logout.html$', account.logout),
    re_path(r'^check_code.html$', account.check_code),
    re_path(r'^login.html$', account.login),
    re_path(r'^$', layout.layout),
    re_path(r'layout.html$', layout.layout),
    re_path(r'^project.html$',project.project),
    re_path(r'project_add.html$', project.project_add),
    re_path(r'project_edit-(\d+).html$', project.project_edit),
    re_path(r'^del_project.html$', project.del_project),
    re_path(r'^resource.html$', resource.resource),
    re_path(r'resource_add.html$', resource.resource_add),
    re_path(r'resource_edit-(\d+).html$', resource.resource_edit),
    re_path(r'^del_resource.html$', resource.del_resource),
    re_path(r'^up_resource.html$', resource.up_resource),
    re_path(r'^resource_select.html$', resource.resource_select),
    re_path(r'^suite.html$', suite.suite),
    re_path(r'suite_add.html$', suite.suite_add),
    re_path(r'suite_edit-(\d+).html$', suite.suite_edit),
    re_path(r'^del_suite.html$', suite.del_suite),
    re_path(r'^up_suite.html$', suite.up_suite),
    re_path(r'^testcase.html$', testcase.testcase),
    re_path(r'testcase_add.html$', testcase.testcase_add),
    re_path(r'testcase_edit-(\d+).html$', testcase.testcase_edit),
    re_path(r'^del_testcase.html$', testcase.del_testcase),
    re_path(r'^keyword.html$', keyword.keyword),
    re_path(r'keyword_add.html$', keyword.keyword_add),
    re_path(r'keyword_edit-(\d+).html$', keyword.keyword_edit),
    re_path(r'^del_keyword.html$', keyword.del_keyword),
    re_path(r'^keywords_select.html$', keyword.keywords_select),
    re_path(r'^library.html$', library.library),
    re_path(r'^up_library.html$', library.up_library),
    re_path(r'^library_detail-(\d+).html$',library.library_detail),
    re_path(r'^del_library.html$', library.del_library),
    re_path(r'^library_init.html$', library.init),
    re_path(r'^run_testcase.html$', runner.run_testcase),
    re_path(r'^stop.html$', runner.stop),
    re_path(r'^run_logs.html$', runner.run_logs),
    re_path(r'^look_report.html$', runner.look_report),
    re_path(r'^report.html$', runner.reportpage),
    re_path(r'^log.html$', runner.logpage),
    re_path(r'project_smpt-(\d+).html$', project.project_smpt),
]

