from .function import check_verification_code
from .models import UserInfo
from django import forms


class ResetPassword(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    code = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)

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

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        # 自定义校验规则
        if len(confirm_password) < 8:
            raise forms.ValidationError("密码长度不能少于8个字符")
        return confirm_password

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        code = self.cleaned_data.get('code')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("两次密码不匹配")
        if username and password:
            try:
                user = UserInfo.objects.get(username=username)
                if not check_verification_code(user.email, code):
                    raise forms.ValidationError("验证码错误")
                if user.username != username:
                    raise forms.ValidationError("用户不能存，不能修改")
                UserInfo.objects.filter(username=username).update(password=password)
            except UserInfo.DoesNotExist:
                raise forms.ValidationError("用户不存在，不能修改")

    class Meta:
        model = UserInfo
        fields = ['username', 'password']
