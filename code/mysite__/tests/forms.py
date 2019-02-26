from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class LoginForm(forms.Form):
    attrs_for_stu_num = {'placeholder': '请输入学号'}
    stu_num = forms.CharField(label='username', max_length=20, widget=forms.TextInput(attrs=attrs_for_stu_num))        # label是在页面上显示的
    pwd = forms.CharField(label='password', initial='请输入密码', widget=forms.PasswordInput)
    jzmm = forms.BooleanField(label='记住密码', widget=forms.CheckboxInput, required=False)

    # widget可以指定参数 如: widget = forms.TextInput(attrs={'class': 'specail'})
    #                       这样就可以在视图中对这个以class='specail'进行渲染
    # attrs:
    #       包含要在呈现的窗口小部件上设置的HTML属性的字典。
    # 1. 对html的属性十分清楚就可以在这里添加很多东西，这次我们添加了placeholder 1.14
    #


class SelectLabForm(forms.Form):
    lab = forms.ChoiceField(label='选择实验室')