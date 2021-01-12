import json
from student.models import Commodities
from django.http import HttpResponse, JsonResponse
from django.template import engines
from log import del_log_stu, get_log_stu
from django.shortcuts import render


django_engine = engines['django']


def display_commodities(request):
    if get_log_stu() is None:
        return render(request, 'login.html')
    # 展示商品
    if request.method == 'GET':
        commodities = Commodities.objects.values('name', 'price', 'commodities_ID')
        commodities = commodities.filter(state=False)
        return render(request, 'home.html', {'commodities': commodities})

    # 退出登录，需要信号量为0
    elif request.method == 'POST':
        signal = json.loads(request.body)['signal']
        if signal == 2:
            del_log_stu()
            if get_log_stu() is None:
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1})
