import hashlib
from .models import Student

def md5(pwd):
    md5_pwd = hashlib.md5(bytes('MyLib', encoding='utf-8'))
    md5_pwd.update(bytes(pwd, encoding='utf-8'))
    return md5_pwd.hexdigest()#返回加密的数据

def update_Data():
    '''
    hash密码储存
    '''
    for stu in Student.objects.all():
        stu.pwd = md5(stu.pwd)
        stu.save()