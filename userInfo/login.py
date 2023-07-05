# 用户登录模块
from django import forms
from .models import UserInfo


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

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

        if username and password:

            try:
                user = UserInfo.objects.get(username=username)
                if user.username == "" or user.password != password:
                    raise forms.ValidationError('Invalid username or password.')
                cleaned_data['user_id']=user.user_id
            except UserInfo.DoesNotExist:
                raise forms.ValidationError('Invalid username or password.')
        return cleaned_data

    class Meta:
        model = UserInfo
        fields = ['username', 'password']
