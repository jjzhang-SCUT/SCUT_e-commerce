from django.db import models


# 教师类（管理员类）
class Teacher(models.Model):
    teacher_ID = models.CharField(max_length=20)  # 教师ID
    name = models.CharField(max_length=20)  # 教师名字
    sex = models.CharField(max_length=20)
    password = models.CharField(max_length=20)  # 密码, 不能为空
