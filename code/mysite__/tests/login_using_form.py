from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import LoginForm, NameForm
from .models import Student, Lab, Instrument, Day, Reservation



# 重写login函数 1.12 22:00

def login(request):
    message = request.method

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            student_num = form.cleaned_data['stu_num'] # 学号
            pwd = form.cleaned_data['pwd']  # 密码

            try:
                student = Student.objects.get(student_num=student_num)
            except Student.DoesNotExist:
                student = None
            if student:
                if student.pwd == pwd:
                    request.session['is_login'] = True
                    request.session['user_id'] = student.id
                    request.session['username'] = student.student_num
                    if student.is_staff:  # 是否是管理员
                        return HttpResponseRedirect(reverse('tests:stf_profile'))
                    return HttpResponseRedirect(reverse('tests:profile'))
                message = '密码错误'
            else:
                message = '用户不存在！'
        form = LoginForm()
        # return render(request, 'tests/login.html', {'message': message})
        return render(request, 'tests/login.html', {'form': form, 'message': message})

    form = LoginForm()
    # message = request.method
    return render(request, 'tests/login.html', {'form': form, 'message': message})