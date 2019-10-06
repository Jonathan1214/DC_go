import random
import hashlib
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db import models
from datetime import datetime
# from .forms import LoginForm, NameForm
from .models import Student, Lab, Instrument, Day, Reservation

# 后期再加
# class_ = ['一班', '二班', '三班', '四班', '五班', '六班', '七班', '八班', '九班', '十班']

# 自己定义一个装饰器好了

def my_login_required(func):
    def check_login_status(request, **kargs):
        '''
        检查登录状态
        '''
        if request.session.has_key('user_id'):
            return func(request, **kargs)
        return redirect(reverse('tests:login'))
    return check_login_status


def md5(pwd):
    md5_pwd = hashlib.md5(bytes('MyLib', encoding='utf-8'))
    md5_pwd.update(bytes(pwd, encoding='utf-8'))
    return md5_pwd.hexdigest()  # 返回加密的数据


def index(request):
    '''
    首次进入 返回登录界面
    '''
    return redirect(reverse('tests:login'))



# def get_name(request):
#     if request.method == 'POST':
#         form = NameForm(request.POST)
#         if form.is_valid():
#             return HttpResponse("good!")
#     else:
#         form = NameForm()
#     return render(request, 'tests/name.html', {'form': form})

# for test


def meta(request):
    '''
    request的使用！
    '''
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    return HttpResponse("Your browser is %s" % ua)

# for test


def login(request):
    '''
    简单登陆界面
    成功则返回：welcome + student_name
    '''
    if request.method == 'POST':
        student_num = request.POST.get("student_num")
        pwd = request.POST.get("password")
        if not student_num:
            return render(request, 'tests/login.html', {'message': '有数据为空！'})
        try:
            student = Student.objects.get(student_num=student_num)
        except Student.DoesNotExist:
            student = None

        if student:
            # 比较 hash 值
            if student.pwd == md5(pwd):
                request.session['is_login'] = True
                request.session['user_id'] = student.id
                request.session['username'] = student.student_num
                if student.is_staff:
                    return HttpResponseRedirect(reverse('tests:stf_profile'))
                return HttpResponseRedirect(reverse('tests:profile'))
            message = '密码错误'
        else:
            message = '用户不存在！'
        return render(request, 'tests/login.html', {'message': message})
    message = ''
    return render(request, 'tests/login.html', {'message': message})


def register(request):
    message = ''
    if request.method == 'POST':
        st_id = request.POST.get("st_id")  # 是否需要验证 id 存在
        st_name = request.POST.get("st_name")
        pwd_first = request.POST.get("pwd_first")
        pwd_again = request.POST.get("pwd_again")

        # if Student.objects.get(student_num=st_id):
        #     message = '学号已存在'
        #     return render(request, 'tests/register.html', {'message': message})

        if pwd_first == pwd_again:
            Student.objects.create(
                student_num=st_id,
                student_name=st_name,
                pwd=md5(pwd_again),
                is_staff=False
            )
            return redirect(reverse('tests:login'))

        message = '两次输入密码不一致'
        return render(request, 'tests/register.html', {'message': message})

    return render(request, 'tests/register.html', {'message': message})


@my_login_required
def logout(request):
    # if not request.session.get('is_login', None):
    #     return redirect()
    request.session.flush()

    return redirect(reverse('tests:login'))


@my_login_required
def profile(request):
    pk = request.session['user_id']
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'tests/user_index.html', {'student': student})

# 装饰器使用,闭包的应用!
# @my_login_required -> check_login_status()
# profile = check_login_status()
# profile() -> 先check_login_status() 再原来的profile()
# 其实也就是check_login_status里面的调用func(),只不过这里的func()是profile()!
# 完全了解!太妙了

# @login_required # 如何正确使用这个装饰器 怎样才算已经登录


@my_login_required
def stf_profile(request):
    stf = Student.objects.get(id=request.session['user_id'])
    return render(request, 'tests/stf_profile.html', {'staff': stf})


@my_login_required
def query_result(request):
    qlab_id = int(request.GET.get('query_lab'))
    qweek_id = int(request.GET.get('query_week'))

    try:
        lab = Lab.objects.get(id=qlab_id)
    except:
        lab = None

    if lab and qweek_id:
        # 按照实验室和星期查询
        res_list = lab.reservation_set.filter(
            week_ord_res=qweek_id).order_by('what_day', 'class_id')
    elif lab:
        res_list = lab.reservation_set.all().order_by(
            'week_ord_res', 'what_day', 'class_id')
        # 应该再加一个排序的 暂时想不到有什么好办法 resolved
    elif qweek_id:
        res_list = Reservation.objects.filter(week_ord_res=qweek_id)
        # 指定周次查询
    else:
        res_list = Reservation.objects.all().order_by(
            'lab__id', 'week_ord_res', 'what_day', 'class_id')
        # 不指定 lab 和周次则查询所有的预约，按照 lab_id 周次 星期 节次 排序
        # 双下划线 means querying across model relation

    return render(request, 'tests/query_result.html', {'lab': lab, 'week': qweek_id, 'res_list': res_list})


@my_login_required
def change_pwd(request):
    pk = request.session['user_id']
    student = Student.objects.get(pk=pk)
    if request.method == 'GET':
        return render(request, 'tests/change_pwd.html', {'student': student})
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')
    if pwd1 == pwd2 and len(pwd1) > 5:
        student.pwd = md5(pwd2)
        student.save()
        return redirect(reverse('tests:profile'))
        # return redirect('tests:login', )
    # 最后要改成一个重定向的页面！
    return render(request, 'tests/change_pwd.html', {'message': '两次输入密码不一致，请重新输入', 'student': student})


@my_login_required
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


@my_login_required
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
        # 实验室是否可以被预约 每节课最多八个人

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


@my_login_required
def my_res(request):
    if request.method == 'POST':
        res_id = request.POST.get('cancel')
        flag = 0
        try:
            res_values = Reservation.objects.filter(id=res_id).values()[0]
            Reservation.objects.get(id=res_id).delete()
            flag = 1
        except:
            return HttpResponse('取消预约失败')

        # 更新预约显示的每节课预约的人数
        if flag:
            lab = Lab.objects.get(id=res_values.get('lab_id'))
            weekday = res_values.get('what_day')
            res_day = lab.day_set.filter(week_ord=res_values.get(
                'week_ord_res'), class_ord=res_values.get('class_id'))[0]
            if weekday == 1:
                res_day.mon_res -= 1
                if res_day.mon_res < 0:
                    res_day.mon_res = 0

            elif weekday == 2:
                res_day.tues_res -= 1
                if res_day.tues_res < 0:
                    res_day.tues_res = 0

            elif weekday == 3:
                res_day.wed_res -= 1
                if res_day.wed_res < 0:
                    res_day.wed_res = 0

            elif weekday == 4:
                res_day.thurs_res -= 1
                if res_day.thurs_res < 0:
                    res_day.thurs_res = 0

            else:
                res_day.fri_res -= 1
                if res_day.fri_res < 0:
                    res_day.fri_res = 0
            res_day.save()

        return redirect(reverse('tests:profile'))

    student = get_object_or_404(Student, id=request.session['user_id'])
    reservations = Reservation.objects.filter(
        student=student)  # 可以获取多个res么 应该可以吧 那这里返回的就是一个数组

    return render(request, 'tests/my_res.html', {'reservations': reservations, 'student': student})


@my_login_required
def contact(request):
    '''
    contact and send email to staff
    '''
    if request.method == 'POST':
        # 邮件头
        subject = request.POST.get('subject', '')
        from_email = request.POST.get('from_email', '')
        # 需要检测这个邮箱是否格式正确
        msg = request.POST.get('feedback', '')
        # 详细发送人
        student = Student.objects.get(id=request.session['user_id'])
        add_msg = '发送人：' + student.student_num + student.student_name
        msg = msg + '\n' + add_msg
        # return HttpResponse(subject)
        to_addr = '407046678@qq.com'

        if msg and from_email and subject:
            try:
                send_mail(subject, msg, from_email, [to_addr])
            except:
                return HttpResponse("Invaild header found")
            return redirect(reverse('tests:profile'))
        else:
            return HttpResponse('请输入正确的信息')
    return render(request, 'tests/contact.html')

@my_login_required
def send_email(request):
    '''
    发送邮件
    '''
    student = Student.objects.get(id=request.session)
    subject = request.GET.get('subject', '')
    msg = request.GET.get('feedback', '')
    from_email = request.GET.get('from_email', '')
    to_addr = '407046678@qq.com'

    if msg and from_email:
        try:
            send_mail(subject, msg, from_email, [to_addr])
        except:
            return HttpResponse("Invaild header found")
        return redirect(reverse('tests:thanks'))
    else:
        return HttpResponse('请输入正确的信息')

