from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .models import Student, Lab, Instrument, Day, Reservation
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import random

def make_reserversion_pre(request):
    '''
    预约界面显示
    '''
    pk = request.session['user_id']
    student = get_object_or_404(Student, pk=pk)
    labs = Lab.objects.all()
    if request.method == 'POST':
        lab_id = request.POST.get('select_lab')
        week_id = request.POST.get('select_week')

        lab = Lab.objects.get(pk=lab_id)

        # 维护一个 4*5 的二维数组，表示没每周每节
        # 放弃这个思路了 直接增加 column
        # 应该是按照周数显示
        return render(request, 'tests/make_2_25.html', {'lab': lab, 'week': week_id, 'student': student})

    return render(request, 'tests/make_res.html', {'student': student, 'labs': labs})


def generate_capta():
    '''
    生成四位随机数验证码
    '''
    a = ''
    for i in range(4):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        a += ch
    return a


def make_reserversion(request):
    '''
    处理预约请求
    '''
    if request.method == 'POST':
        # 获取各种id
        req_inst = request.POST.getlist('inst_list', [])    # 仪器
        req_lab_cls = request.POST.get('res')
        lab_id = int(req_lab_cls[0])           # 实验室
        weekday = int(req_lab_cls[1])          # 星期
        class_id = int(req_lab_cls[2])         # 节次
        week_ord = int(req_lab_cls[3])         # 周
        student_id = request.session['user_id']
        capta = generate_capta()
        # 获取预约的内容
        student = Student.objects.get(pk=student_id)
        lab = Lab.objects.get(pk=lab_id)

        if req_inst:
            yiqi = Instrument.objects.get(pk=req_inst[0])
        else:
            yiqi = None

        # week_ord_res = models.IntegerField.create(week_ord)
        # what_day = models.IntegerField.objects.create(weekday)

        # 这里应该要加上一个try排错才好

        # 几个判断条件
        # 1.每节课的预约人数不能超过上限 最多 8 人每节课
        # 2.每个人的预约次数有上限 不如就一周三次
        # 3.一个人不能预约重复预约一个教室

        man_can_reserve = 1 if len(Reservation.objects.filter(
            student=student, week_ord_res=week_ord)) < 3 else 0
        # 教室
        hasnt_reserved_the_class = 1 if not Reservation.objects.filter(
            student=student, week_ord_res=week_ord, what_day=weekday, class_id=class_id) else 0
        # 是否已经预约了这个教室
        class_can_reservered = 1 if len(Reservation.objects.filter(
            lab=lab, week_ord_res=week_ord, what_day=weekday, class_id=class_id)) < 8 else 0

        if man_can_reserve and class_can_reservered and hasnt_reserved_the_class:
            Reservation.objects.create(
                student=student,
                lab=lab,
                yiqi=yiqi,
                week_ord_res=week_ord,
                class_id=class_id,
                what_day=weekday,
                res_time=datetime.now(),
                capta=capta
            )

            if yiqi:
                yiqi.used += 1
                yiqi.save()

            res_day = lab.day_set.filter(
                week_ord=week_ord, class_ord=class_id)[0]
            if weekday == 1:
                res_day.mon_res += 1
            elif weekday == 2:
                res_day.tues_res += 1
            elif weekday == 3:
                res_day.wed_res += 1
            elif weekday == 4:
                res_day.thurs_res += 1
            else:
                res_day.fri_res += 1
            res_day.save()

            # 这里用名称更好 redirect(reverse('tests:profile'))
            # 发送邮件
            subject = "预约验证码"
            from_email = settings.DEFAULT_FROM_EMAIL
            send_msg = {'week': week_ord, 'whatday': weekday, 'class_id': class_id, 'lab': lab.name,
                        'address': lab.address, 'capta': capta}
            msg = "您预约第{week}周星期{whatday}第{class_id}节课在{lab}（地址：{address}）的实验已经生效，进入实验室的验证码为：{capta}，请按时去实验室完成实验。\n祝您好运\
                \n              MyLab团队".format(**send_msg)
            to_addr = '{}@stu.hit.edu.cn'.format(student.student_num)
            try:
                send_mail(subject, msg, from_email, [to_addr])
                send_mail('发送失败', '预约邮件发送成功，注意查看',
                          from_email, ['407046678@qq.com'])
            except:
                send_mail('发送失败', '预约邮件发送失败，注意查看。原邮件内容：'+msg,
                          from_email, ['407046678@qq.com'])
            #############################
            return redirect(reverse('tests:profile'))

        elif man_can_reserve:
            message = "当前教室无法预约或您已经预约此教室"
        else:
            message = "本周预约次数已到达上限"

        return HttpResponse(message)
