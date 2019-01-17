from django.db import models

# Create your models here.


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=32)


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=32)
    cid = models.ManyToManyField(Class, name="teacher")
    # name 是做正向查询时用的
    # related_name 是做反向查询用的
    # 如：
    #    假设两个表已经连接好 Class有c1 Teacher有t1
    #    正向查询：未指定name 则使用t1.cid即可查询 否则使用t1.name查询
    #    反向查询：未指定reated_name 则c1.teacher_set可查询 否则使用c1.related_name查询
    #    注意一个十分具有欺骗性的坑，当仅仅创建两个表时，他们并没有连接在一起，而这个时候进行c1.teacher_set仍可以得到返回对象
    #        但是使用c1.teacher_set.all时，查询结果为空，在使用c1.teacher_set.add(t1)之后，进行c1.teacher_set.all查询才
    #        得到正确的返回


class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

    def __str__(self):
        return self.name

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)
