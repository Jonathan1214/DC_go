# import logging
from django.http import HttpResponse, Http404
# from django.template import loader
from django.shortcuts import render
from .models import Question
# logging 用来产生日志 我觉得这个很有必要！记录！

def index(request):
    '''
    主界面
    '''
    # return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def baidu(request):
    '''
    返回一个baid搜索的界面 测试用
    '''
    return render(request, 'polls/baidu.html')

def detail(request, question_id):
    '''
    问题详情
    '''
    # return HttpResponse("You're looking at question %s." % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    '''
    投票结果
    '''
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    '''
    投票
    '''
    return HttpResponse("You're voting on question %s." % question_id)

def add(request):
    '''
    加法运算
    '''
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))
