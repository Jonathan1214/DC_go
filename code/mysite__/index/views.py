import sys
import hashlib
sys.path.append("..")
# from tests.models import Student
from .models import IMG, MyUser
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# def home(request):
#     students = Student.objects.all()
#     return render(request, 'index/home.html', {'students': students})

def md5(pwd):
    md5_pwd = hashlib.md5(bytes('MyLib', encoding='utf-8'))
    md5_pwd.update(bytes(pwd, encoding='utf-8'))
    return md5_pwd.hexdigest()  # 返回加密的数据

def register(request):
    message = ''
    if request.method == 'POST':
        account = request.POST.get("account")  # 是否需要验证 id 存在
        pwd_first = request.POST.get("pwd_first")
        pwd_again = request.POST.get("pwd_again")

        # if Student.objects.get(student_num=st_id):
        #     message = '学号已存在'
        #     return render(request, 'tests/register.html', {'message': message})

        if pwd_first == pwd_again:
            MyUser.objects.create(
                account=account,
                pwd=md5(pwd_again)
            )
            return redirect(reverse('index:login'))

        message = '两次输入密码不一致'
        return render(request, 'index/register.html', {'message': message})

    return render(request, 'index/register.html', {'message': message})

def login(request):
    '''
    简单登陆界面
    成功则返回：welcome + student_name
    '''
    if request.method == 'POST':
        account = request.POST.get("account")
        pwd = request.POST.get("password")
        if not account:
            return render(request, 'index/login2.html', {'message': '有数据为空！'})
        try:
            my_user = MyUser.objects.get(account=account)
            # student = Student.objects.get(student_num=student_num)
        except MyUser.DoesNotExist:
            my_user = None

        if my_user:
            # 比较 hash 值
            if my_user.pwd == md5(pwd):
                request.session['is_login'] = True
                request.session['user_id'] = my_user.id
                request.session['username'] = my_user.account
                # if student.is_staff:
                #     return HttpResponseRedirect(reverse('tests:stf_profile'))
                return redirect(reverse('index:show_img'))
            message = '密码错误'
        else:
            message = '用户不存在！'
        return render(request, 'index/login2.html', {'message': message})
    message = ''
    return render(request, 'index/login2.html', {'message': message})

# @csrf_exempt
def uploading(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
        return redirect(reverse('index:show_img'))
    return render(request, 'index/upload_img.html')

def show_img(request):
    imgs = IMG.objects.all()
    return render(request, 'index/showing_img.html', {'imgs':imgs})
        # <!-- <img src="{% media 'images/head2.jpg' %}" -->