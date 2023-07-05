from django import forms
from django.forms.utils import ErrorList

from userInfo.models import UserInfo


# 修改用户密码

class ModifyUserPassword(forms.ModelForm):
    username = forms.CharField()
    old_password = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 自定义校验规则
        if len(username) < 5:
            raise forms.ValidationError("用户名长度不能少于5个字符")
        return username

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        # 自定义校验规则
        if len(old_password) < 8:
            raise forms.ValidationError("密码长度不能少于8个字符")
        return old_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # 自定义校验规则
        if len(password) < 8:
            raise forms.ValidationError("密码长度不能少于8个字符")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        # 自定义校验规则
        if len(confirm_password) < 8:
            raise forms.ValidationError("密码长度不能少于8个字符")
        return confirm_password

    def clean(self):
        username = self.cleaned_data.get("username")
        old_password = self.cleaned_data.get('old_password')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        print(username, old_password, password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("两次密码不匹配")

        if username and old_password and password:
            try:
                user = UserInfo.objects.get(username=username)
                print(user.username,user.password,old_password)
                if user.username != username:
                    raise forms.ValidationError("用户不能存，不能修改")
                if user.password != old_password:
                    raise forms.ValidationError("原密码错误")
                print(user.password)
                UserInfo.objects.filter(username=username).update(password=password)
            except UserInfo.DoesNotExist:
                raise forms.ValidationError("用户不存在，不能修改")

    class Meta:
        model = UserInfo
        fields = ['username', 'password']
