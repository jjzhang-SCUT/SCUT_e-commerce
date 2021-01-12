import json
from teacher.models import Teacher
from django.http import HttpResponse, JsonResponse
from django.template import engines
from log import get_log_admin
from django.shortcuts import render


django_engine = engines['django']


# admin/profile
def display_profile(request):
    try:
        get_log_admin().teacher_ID
    except:
        return render(request, 'login.html')
    # 展示个人信息
    if request.method == 'GET':
        teacher = Teacher.objects.values('teacher_ID', 'name', 'sex')
        teacher = teacher.filter(teacher_ID=str(get_log_admin().teacher_ID))

        return render(request, 'profile.html', {'teachers': teacher})

    # 修改个人信息
    elif request.method == 'POST':
        info = json.loads(request.body)['data']
        my = get_log_admin()
        if 'name' in info:
            my.name = info['name']
        if 'sex' in info:
            my.sex = info['sex']
        if 'password' in info:
            my.password = info['password']

        my.save()
        return JsonResponse({'ret': 0})
