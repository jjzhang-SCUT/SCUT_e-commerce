from django.http import JsonResponse
from django.shortcuts import render

from teacher.models import Teacher
from student.models import Student
import json

log_stu = None
log_admin = None


def get_log_admin():
    return log_admin


def del_log_admin():
    global log_admin
    log_admin = None


def get_log_stu():
    return log_stu


def del_log_stu():
    global log_stu
    log_stu = None


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    my_id = json.loads(request.body)['username']
    password = json.loads(request.body)['password']
    user = Teacher.objects.filter(teacher_ID=my_id)
    # 0 学生正常登陆 1 教师正常登录 2 密码错误 3 账户不存在
    if user:
        user = Teacher.objects.get(teacher_ID=my_id)
        if user.password == password:
            global log_admin
            log_admin = user
            return JsonResponse({'ret': 1})
        else:
            return JsonResponse({'ret': 2, 'msg': "Wrong Password"})
    else:
        user = Student.objects.filter(student_ID=my_id)
        if user:
            user = Student.objects.get(student_ID=my_id)
            if user.password == password:
                global log_stu
                log_stu = user
                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 2, 'msg': "Wrong Password"})
        else:
            return JsonResponse({'ret': 3, 'msg': "Account not exist"})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    info = json.loads(request.body)['data']
    is_exist = Student.objects.filter(student_ID=info['student_ID'])
    if is_exist:
        return JsonResponse({'ret': 1, 'msg': 'User exist'})
    record = Student.objects.create(student_ID=info['student_ID'],
                                    name=info['name'],
                                    sex=info['sex'],
                                    college=info['college'],
                                    major=info['major'],
                                    dormitory=info['dormitory'],
                                    telephone=info['telephone'],
                                    password=info['password'])
    return JsonResponse({'ret': 0})
