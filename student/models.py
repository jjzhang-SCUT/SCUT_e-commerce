from django.db import models


# 学生类
class Student(models.Model):
    student_ID = models.CharField(max_length=13)  # 学生ID为12为的学号, 如‘201830570095’
    telephone = models.CharField(max_length=13)  # 电话号码
    name = models.CharField(max_length=10)  # 学生姓名, 不能为空
    sex = models.CharField(max_length=10)
    college = models.CharField(max_length=20)  # 学院
    major = models.CharField(max_length=20)  # 专业
    dormitory = models.CharField(max_length=20)  # 宿舍号
    password = models.CharField(max_length=20)  # 密码, 不能为空


# 商品类
class Commodities(models.Model):
    commodities_ID = models.CharField(max_length=20)  # 商品ID, 系统生成
    seller_ID = models.CharField(max_length=20)  # 卖家ID（学生ID）
    name = models.CharField(max_length=20)  # 商品名字
    price = models.CharField(max_length=20)  # 商品价格
    description = models.CharField(max_length=200)  # 商品描述
    inventory = models.IntegerField()  # 库存
    state = models.BooleanField(default=False)  # True 说明商品已被删除, 商品不可见


# 订单类
class Order(models.Model):
    order_ID = models.CharField(max_length=20)  # 订单ID，系统生成
    buyer_ID = models.CharField(max_length=20)  # 买家ID（学生ID）
    consignee = models.CharField(max_length=20)  # 收货人
    telephone = models.CharField(max_length=20)  # 收货联系电话
    address = models.CharField(max_length=20)  # 收货地址（宿舍号）
    seller_ID = models.CharField(max_length=20)  # 卖家ID（学生ID）
    commodities = models.ForeignKey(Commodities, on_delete=models.PROTECT)  # 商品类的外键
    time = models.DateTimeField(auto_now_add=True)  # 订单创建时间
    state = models.BooleanField(default=False)  # state=0为已付款, state=1为确认收货

    class Meta:
        ordering = ['-time']  # 订单按照创建时间倒序排序, 即新订单排在前面


# 评论类
class Comment(models.Model):
    buyers_ID = models.CharField(max_length=20)  # 买家ID
    commodities_ID = models.CharField(max_length=20)  # 商品ID
    comment = models.CharField(max_length=200)  # 评论
