import json

from django.shortcuts import render

from student.models import Student
from django.http import HttpResponse, JsonResponse
from log import get_log_stu


# home/profile
def display_profile(request):
    if get_log_stu() is None:
        return render(request, 'login.html')
    # 展示个人信息
    if request.method == 'GET':
        student = Student.objects.values('student_ID', 'name', 'sex', 'college', 'major', 'dormitory', 'telephone', 'password')
        student = student.filter(student_ID=str(get_log_stu().student_ID))
        if 'editing' in request.GET and request.GET['editing'] == 'True':
            return render(request, 'profile.html', {'student': student, 'edit': 'true'})
        return render(request, 'profile.html', {'student': student, 'edit': 'false'})

    # 修改个人信息
    elif request.method == 'POST':
        info = request.POST
        my = get_log_stu()
        if 'name' in info:
            my.name = info['name']
        if 'sex' in info:
            my.sex = info['sex']
        if 'college' in info:
            my.college = info['college']
        if 'major' in info:
            my.major = info['major']
        if 'dormitory' in info:
            my.dormitory = info['dormitory']
        if 'password' in info:
            my.password = info['password']
        if 'telephone' in info:
            my.telephone = info['telephone']

        my.save()
        return render(request, 'profile.html', {'student': [my], 'edit': 'false'})
