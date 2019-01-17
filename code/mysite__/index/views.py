import sys
sys.path.append("..")
from tests.models import Student
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

def home(request):
    students = Student.objects.all()
    return render(request, 'index/home.html', {'students': students})

def login(request):
    pass
