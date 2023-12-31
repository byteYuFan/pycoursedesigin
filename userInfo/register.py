# 用户注册
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
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')

        if username and password and email:
            try:
                user_with_username = UserInfo.objects.get(username=username)
                raise forms.ValidationError('Username already exists.')
            except UserInfo.DoesNotExist:
                pass

            try:
                user_with_email = UserInfo.objects.get(email=email)
                raise forms.ValidationError('Email already exists.')
            except UserInfo.DoesNotExist:
                pass

        return cleaned_data

    class Meta:
        model = UserInfo
        fields = ['username', 'password', 'email']
