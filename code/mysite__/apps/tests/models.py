from django.db import models

# Create your models here.


class Student(models.Model):
    student_num = models.CharField(max_length=10)
    student_name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=30)

    def __str__(self):
        return self.student_name


# 实验室
class Lab(models.Model):
    name = models.CharField(max_length=10)  # 实验室名字
    address = models.CharField(max_length=50)  # 实验室地址

    # 实验室和学生关联起来 表示预约 被迫用拼音？？？
    yuyue = models.ManyToManyField(
        Student, through='Reservation', through_fields=('lab', 'student'))

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(max_length=20)
    total = models.IntegerField(default=4) # 总数
    used = models.IntegerField(default=0)  # 已经使用数量
    # 把实验室和仪器关联起来 方便查询
    to_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Day(models.Model):
    class_ord = models.IntegerField(default=0)       # 节次 设定为4节 上下午各两节
    mon_cls = models.IntegerField(default=0)       # 改成预约的人数 默认为0 表示无人预约
    tues_cls = models.IntegerField(default=0)       # 设置上限为10？ 这个后面具体考察
    wed_cls = models.IntegerField(default=0)       # 当值超过10时表示教室在上课 被占用
    thurs_cls = models.IntegerField(default=0)
    fri_cls = models.IntegerField(default=0)

    week_ord = models.IntegerField(default=1)
    #  课程时间什么的直接在HTML里面写 省去了
    day_to_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.week_name


# 预约表 把学生和实验室关联起来
class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    # 预约仪器
    yiqi = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True, blank=True)

    week_ord_res = models.IntegerField(default=1)
    what_day = models.IntegerField(default=1) # 星期几 从星期一到星期天

# class class_time(models.Model):
    # start = models.TimeField()  # 开始时间 其实这张表都是不可更改的
    # duration = models.DurationField()


# 花里胡哨的东西都不要加了 什么meta啊 元啊！在后期有时间再来修改 让这个东西更加完美
