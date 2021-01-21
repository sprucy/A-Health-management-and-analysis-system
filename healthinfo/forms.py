from django import forms
from . import models

class UserLoginForm(forms.Form):
    username = forms.CharField(label="用户名",max_length=128,min_length=4,required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名长度不得超过128个字符',
            'min_length': '用户名长度不得少于4个字符',},
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, min_length=6,required=True, 
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不得超过256个字符',
            'min_length': '密码长度不得少于8个字符',},
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))

class UserRegistForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128,min_length=4,required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名长度不得超过128个字符',
            'min_length': '用户名长度不得少于4个字符',},
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, min_length=8, required=True,
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不得超过256个字符',
            'min_length': '密码长度不得少于8个字符',},
        widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    password1 = forms.CharField(label="确认密码", max_length=256, min_length=8, required=True, 
        error_messages={
            'required': '密码不能为空',
            'max_length': '密码长度不得超过256个字符',
            'min_length': '密码长度不得少于8个字符',},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
        
'''

'''


class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo    #与models建立了依赖关系
        fields = "__all__"
        labels = {
            'name':'姓名', 
            'birthday':'出生日期',
            'sex':'性别',
            'phone':'电话',
            'org':'单位',
            'smoke':'吸烟',
            'diabetes':'糖尿病',
            'photo': '照片',
        }
        error_messages = {
            'name':{
                'required':'姓名不能为空',
            }
        }