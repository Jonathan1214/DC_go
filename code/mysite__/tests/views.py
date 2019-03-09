from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import models
from datetime import datetime
from .forms import LoginForm, NameForm
from .models import Student, Lab, Instrument, Day, Reservation


# 自己定义一个装饰器好了
def my_login_required(func):
    def check_login_status(request, **kargs):
        '''
        检查登录状态
        '''
        if request.session.has_key('user_id'):
            return func(request, **kargs)
        return redirect('/tests/login/')
    return check_login_status


def index(request):
    '''
    return 'hello world'
    '''
    return HttpResponse("hello world")

# for test


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse("good!")
    else:
        form = NameForm()
    return render(request, 'tests/name.html', {'form': form})

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
            if student.pwd == pwd:
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
    return render(request, 'tests/login.html', {'message': '重新输入！'})

# 重写login函数 1.12 22:00


# def login(request):
#     message = request.method

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             student_num = form.cleaned_data['stu_num'] # 学号
#             pwd = form.cleaned_data['pwd']  # 密码

#             try:
#                 student = Student.objects.get(student_num=student_num)
#             except Student.DoesNotExist:
#                 student = None
#             if student:
#                 if student.pwd == pwd:
#                     request.session['is_login'] = True
#                     request.session['user_id'] = student.id
#                     request.session['username'] = student.student_num
#                     if student.is_staff:  # 是否是管理员
#                         return HttpResponseRedirect(reverse('tests:stf_profile'))
#                     return HttpResponseRedirect(reverse('tests:profile'))
#                 message = '密码错误'
#             else:
#                 message = '用户不存在！'
#         form = LoginForm()
#         # return render(request, 'tests/login.html', {'message': message})
#         return render(request, 'tests/login.html', {'form': form, 'message': message})

#     form = LoginForm()
#     # message = request.method
#     return render(request, 'tests/login.html', {'form': form, 'message': message})


@my_login_required
def logout(request):
    # if not request.session.get('is_login', None):
    #     return redirect()
    request.session.flush()

    return redirect('/tests/login/')


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
    # 管理员显示页面
    # if request.method == "GET":
    #     qlab_id = int(request.GET.get('query_lab'))
    #     qweek_id = int(request.GET.get('query_week'))

    #     lab = Lab.objects.get(id=qlab_id)
    #     return render(request, 'tests/query.html', {'lab': lab, 'week': qweek_id})

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
        res_list = lab.reservation_set.filter(week_ord_res=qweek_id).order_by('what_day')
    elif lab:
        res_list = lab.reservation_set.all() # 应该再加一个排序的 暂时想不到有什么好办法
    elif qweek_id:
        res_list = Reservation.objects.filter(week_ord_res=qweek_id)
    else:
        res_list = Reservation.objects.all()

    return render(request, 'tests/query_result.html', {'lab': lab, 'week': qweek_id, 'res_list': res_list})


@my_login_required
def change_pwd(request):
    if request.method == 'GET':
        return render(request, 'tests/change_pwd.html')
    pk = request.session['user_id']
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')
    if pwd1 == pwd2 and len(pwd1) > 5:
        student = Student.objects.get(pk=pk)
        student.pwd = pwd2
        student.save()
        return HttpResponseRedirect('/tests/login/')
        # return redirect('tests:login', )
    # 最后要改成一个重定向的页面！
    return render(request, 'tests/change_pwd.html', {'message': '两次输入密码不一致，请重新输入'})


@my_login_required
def make_reserversion_pre(request):
    '''
    预约界面显示
    '''
    if request.method == 'POST':
        lab_id = request.POST.get('select_lab')
        week_id = request.POST.get('select_week')

        lab = Lab.objects.get(pk=lab_id)
        # 应该是按照周数显示
        return render(request, 'tests/make_2_25.html', {'lab': lab, 'week':week_id})

    pk = request.session['user_id']
    student = get_object_or_404(Student, pk=pk)
    labs = Lab.objects.all()
    return render(request, 'tests/make_res.html', {'student': student, 'labs': labs})



@my_login_required
def make_reserversion(request):
    '''
    处理预约请求
    '''
    if request.method == 'POST':
        # 获取各种id
        req_inst = request.POST.getlist('inst_list', [])    # 仪器
        req_lab_cls = request.POST.get('res')
        lab_id = int(req_lab_cls[0])
        weekday = int(req_lab_cls[1])
        class_id = int(req_lab_cls[2])
        week_ord = int(req_lab_cls[3])
        student_id = request.session['user_id']

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
        Reservation.objects.create(
            student=student,
            lab=lab,
            yiqi=yiqi,
            week_ord_res=week_ord,
            class_id=class_id,
            what_day=weekday,
            res_time=datetime.now()
        )

        if yiqi:
            yiqi.used += 1

        # 这里用名称更好 redirect(reverse('tests:profile'))
        return redirect('/tests/profile/')



@my_login_required
def my_res(request):
    if request.method == 'POST':
        res_id = request.POST.get('cancel')
        try:
            Reservation.objects.filter(id=res_id).delete()
            # res.student.clear()
            # res.lab.clear()
            # res.yiqi.clear()
        except:
            return HttpResponse('取消预约失败')
        return redirect('/tests/profile/')

    student = get_object_or_404(Student, id=request.session['user_id'])
    reservations = Reservation.objects.filter(
        student=student)  # 可以获取多个res么 应该可以吧 那这里返回的就是一个数组

    return render(request, 'tests/my_res.html', {'reservations': reservations})


@my_login_required
def cancelres(request):
    if request.method == 'POST':
        pass
        redirect('/tests/profile/')
