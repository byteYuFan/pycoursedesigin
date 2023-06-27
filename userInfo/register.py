# 用户注册
from django import forms
from .models import UserInfo
from django import forms

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 自定义校验规则
        if len(username) < 5:
            raise forms.ValidationError("用户名长度不能少于5个字符")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # 自定义校验规则
        if len(password) < 8:
            raise forms.ValidationError("密码长度不能少于8个字符")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')
        # 自定义校验规则
        if password and email:
            if password.lower() in email.lower():
                raise forms.ValidationError("密码不能包含邮箱地址")
        return cleaned_data

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'email']
