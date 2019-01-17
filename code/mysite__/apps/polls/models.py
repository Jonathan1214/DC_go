from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    qq = models.ForeignKey(Question, on_delete=models.CASCADE) # 这又是什么意思呢？ 只
                                                            #    是一个名字罢了 其实没什么作用…… 很不想这么说
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# 创建django的model时，有DateTimeField、DateField和TimeField三种类型可以用来创建日期字段，
# 其值分别对应着datetime()、date()、time()三中对象。这三个field有着相同的参数auto_now和auto_now_add，
# 表面上看起来很easy，但实际使用中很容易出错，下面是一些注意点。

