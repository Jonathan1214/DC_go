from django.db import models

# Create your models here.


class Student(models.Model):
    student_num = models.CharField(max_length=10)
    student_name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)

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
    total = models.IntegerField(default=4)  # 总数
    used = models.IntegerField(default=0)  # 已经使用数量
    # 把实验室和仪器关联起来 方便查询
    to_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Day(models.Model):
    class_ord = models.IntegerField(default=0)       # 节次 设定为4节 上下午各两节
    week_ord = models.IntegerField(default=1)

    # 定义 如果不是为了那个该死的上课时间导入，我又怎么会写这个恶心的表
    # 是不是应该考虑周末，似乎一般周末才有时间
    mon_cls = models.IntegerField(default=0)       # 改成预约的人数 默认为0 表示无人预约
    tues_cls = models.IntegerField(default=0)       # 设置上限为10？ 这个后面具体考察
    wed_cls = models.IntegerField(default=0)       # 当值超过10时表示教室在上课 被占用
    thurs_cls = models.IntegerField(default=0)
    fri_cls = models.IntegerField(default=0)

    mon_res = models.IntegerField(default=0, null=True)
    tues_res = models.IntegerField(default=0, null=True)
    wed_res = models.IntegerField(default=0, null=True)
    thurs_res = models.IntegerField(default=0, null=True)
    fri_res = models.IntegerField(default=0, null=True)

    #  课程时间什么的直接在HTML里面写 省去了
    day_to_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.week_name
    # 我到现在也不太明白这个表的作用，但是当初是什么东西促使我写下这个表呢，我想不太起来了，只知道它一定有着不可替代的作用

# 预约表 把学生和实验室关联起来
class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True)

    # 预约仪器
    yiqi = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, null=True)
    # 可以为空

    week_ord_res = models.IntegerField(default=1) # 第几周
    what_day = models.IntegerField(default=1)  # 星期几 从星期一到星期天
    class_id = models.IntegerField(null=True)

    res_time = models.DateTimeField(null=True)

    capta = models.CharField(max_length=4, null=True)

# class class_time(models.Model):
    # start = models.TimeField()  # 开始时间 其实这张表都是不可更改的
    # duration = models.DurationField()


# 花里胡哨的东西都不要加了 什么meta啊 元啊！在后期有时间再来修改 让这个东西更加完美
