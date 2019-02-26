# coding:utf-8
# 学生信息已经输入好了
# 现在把这个表构建好 试着运行一下
#
from .models import Lab, Student, Instrument, Reservation, Day


def initial_lab():
    lab_name = ['lab1', 'lab2', 'lab3']
    lab_address = ['主楼1', '主楼2', '新技术楼3']

    for i in range(3):
        Lab.objects.create(
            name=lab_name[i], address=lab_address[i])


def initial_instrument():
    '''
    初始化仪器类
    包括：示波器，稳压源，万用表……
    先用这三个
    '''
    # 已经指定了默认值 就不用管数量了
    instrument_name = ['示波器', '稳压源', '万用表']

    for i in range(len(instrument_name)):
        Instrument.objects.create(name=instrument_name[i])


def initial_day():
    week_name = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天']
    for i in range(len(week_name)):
        Day.objects.create(week_name=week_name[i])


# 所以和外键连接起来的初始化的时候就要指定连接