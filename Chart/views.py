from django.shortcuts import render
from django.http import JsonResponse
from repository import models
from django.db.models import Avg,Count,Min,Max,Sum
from django.core import serializers
import json
from django.shortcuts import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


def chart(request):
    if request.method == "POST":
        Suitecount = models.Suite.objects.values_list('project').annotate(sc=Count('id'))
        p_s = json.dumps(list(Suitecount.values('project__project_name', 'sc')), cls=DjangoJSONEncoder)
        Casecount = models.Testcase.objects.values_list('suite__project').annotate(c=Count('id'))
        print(type(Casecount.values('suite__project__project_name', 'c')))
        p_c = json.dumps(list(Casecount.values('suite__project__project_name', 'c')), cls=DjangoJSONEncoder)
        # 返回数据
        return JsonResponse({'p_s':p_s,'p_c':p_c})
    else:
        return render(request, 'chart.html',)