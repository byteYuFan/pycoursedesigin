# Django实战

![](https://img.shields.io/badge/python-v3.8-blue)

![](https://img.shields.io/badge/auth-wyf-red)

## 1. 项目介绍



## 2. 项目搭建


```shell
# 创建一个Django项目，命名位course
django-admin startproject course
# 创建一个用户服务应用 
 python manage.py startapp userInfo
```

### 2.1. 基础配置

#### 1. 项目配置

​		为了在我们的工程中包含这个应用，我们需要在配置类 `INSTALLED_APPS`中添加设置。因为 `UserInfoConfig` 类写在文件 `UserInfo/apps.py` 中，所以它的点式路径是 `'userInfo.apps.UserInfoConfig'`。在文件 `course/settings.py` 中 `INSTALLED_APPS`子项添加点式路径后，它看起来像这样：

```cfg

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userInfo.apps.UserinfoConfig'
]

```

#### 2. 数据库配置(MySQL)

```shell
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "python",
        "USER": "user",
        "PASSWORD": "***********",
        "HOST": "xxxxxxxxxx",
        "PORT": "3306",
    }
}
```

#### 3. 邮件模块配置(163)

```shell
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 25
# 邮箱配置
EMAIL_HOST_USER = '18091323970@163.com'  # 配置邮箱
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxx'  # 对应的授权码
```

#### 4. Redis 配置

```shell
def get_redis_connection():
    redis_host = 'localhost'
    redis_port = 6379
    redis_password= ""
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port,password=redis_password, db=redis_db)
    return redis_client
```

#### 5. 静态资源配置

```shell
STATIC_URL = '/static/'
```

#### 6. 访问权限配置

```shell
ALLOWED_HOSTS = ['*']
```

### 2.2. 模型迁移

```shell
# 模型激活
$python manage.py makemigrations userInfo
# 输出
Migrations for 'userInfo':
  userInfo\migrations\0001_initial.py
    - Create model UserInfo
```

```shell
# 将结果迁移到数据库中去
python manage.py migrate
```

### 2.3. 开启超级用户模式
```shell
$python manage.py createsuperuser
```

![](./images/1-admin.png)

![](./images/1-enteradmin.png)

## 3. 用户模型

### 3.1. 模型介绍

用户信息模型目前有以下五个内容：`user_id`,`username`,`password`,`email`,`flag`,`time`

-`user_id`：由数据库自动制定
-`username`：用户名
-`password`：用户密码
-`email`：用户邮箱
-`flag`：是否删除标志，默认为`false`
-`time`：用户账户过期时间

```python
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    flag = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
```

- `user_id` 字段使用了 `AutoField`，它是一个自动递增的整数字段，作为主键。
- `username` 字段使用了 `CharField`，它表示一个字符型字段，最大长度为 255。
- `password` 字段使用了 `CharField`，表示用户密码字段，最大长度为 255。
- `email` 字段使用了 `EmailField`，表示用户邮箱字段，验证输入的值是否为有效的邮箱格式。
- `flag` 字段使用了 `BooleanField`，表示一个布尔类型字段，默认值为 `False`，表示未删除状态。
- `time` 字段使用了 `DateTimeField`，表示一个日期时间类型字段，允许为 `null` 值，用于表示用户账户的过期时间。

```shell
# 模型激活
$ python manage.py makemigrations userInfo
# 输出
Migrations for 'userInfo':
  userInfo\migrations\0001_initial.py
    - Create model UserInfo

```

​		通过运行 `makemigrations` 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次*迁移*。

```shell
# 可视化迁移结果
$ python manage.py sqlmigrate userInfo 0001
```

```mysql

BEGIN;
--
-- Create model UserInfo
--
CREATE TABLE "userInfo_userinfo" ("user_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "username" varchar(255) NOT NULL, "password" varchar(255) NOT NULL, "email" varchar(254) NOT NULL, "flag" bool NOT NULL, "time" datetime NULL);
COMMIT;

```

```shell
# 将结果迁移到数据库中去
python manage.py migrate
```

### 3.2. 发送邮件功能

#### 1. view

```python
def send_email_verification(request):
    if request.method == "POST":
        email = request.POST.get("email")  # 获取前端传递的邮箱地址
        subject = 'NAT验证码'
        message = generate_verification_code()
        store_verification_code(email, message)
        from_email = '18091323970@163.com'
        # 执行发送邮箱验证码的逻辑
        send_mail(subject, message, from_email, [email])
        return JsonResponse({"message": "邮箱验证码发送成功", "success": True})
    else:
        return JsonResponse({"message": "请求方法不支持", "success": False})
```

这段代码是一个`Django`视图函数，用于处理发送邮件验证码的请求。它包含这样的逻辑：

1. 首先，它检查请求的方法是否为POST，如果不是，则返回一个JSON响应表示请求方法不支持。
2. 如果请求方法为POST，它从请求的POST数据中获取邮箱地址，并调用`generate_verification_code`生成一个验证码。
3. 然后，它调用`store_verification_code`函数将邮箱地址和验证码存储到`Redis`中。
4. 接下来，它设置了邮件的主题和消息内容。
5. 然后，它指定了发送方的邮箱地址。
6. 最后，它调用`send_mail`函数发送邮件，将主题、消息、发送方邮箱和接收方邮箱作为参数。
7. 如果发送邮件成功，它返回一个JSON响应表示邮件验证码发送成功。

#### 2. urls

```python
 path('send-email-verification/', views.send_email_verification, name='send_email_verification')
```

#### 3. 函数说明

**随机生成验证码函数:**

```python	
def generate_verification_code(length=6):
    characters = string.digits  # 仅包含数字的字符集
    code = ''.join(random.choice(characters) for _ in range(length))
    return code
```

**存储到Redis函数:**

```python
def store_verification_code(email, code, expire_time=300):
    redis_client = get_redis_connection()
    redis_key = email
    redis_client.set(redis_key, code, ex=expire_time)
```

#### 4. 功能测试

```js
$(document).ready(function () {
            $("#sendButton").click(function () {
                startCountdown()
                let csrftoken = getCookie('csrftoken');
                $.ajax({
                    url: "{% url 'send_email_verification'  %}",  // Django后端的URL
                    method: "POST",
                    headers: {"X-CSRFToken": csrftoken},  // 在请求头中包含CSRF令牌
                    data: {email: document.getElementById("email").value},  // 将邮箱地址作为数据发送
                    success: function (response) {
                        alert(response.message);  // 弹出成功信息
                    },
                    error: function () {
                        alert("发送邮件失败");  // 弹出错误信息
                    }
                });
            })
})
```

![](./images/2-sendemail-test.png)

![](./images/2-code.png)

![](./images/2-redis.png)

### 3.3. 用户注册功能

#### 1. 模型建立

**Django 提供了一个辅助类让你可以从一个 Django 模型创建一个 Form 类。**

于是我们创建了名称为`UserRegistrationForm`的 Form类如下所示：
```python
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
	email = forms.EmailField()

class Meta:
    model = UserInfo
    fields = ['username', 'password', 'email']
```

**Meta类用于提供额外的元数据（metadata），以指定表单的行为和特性。**Meta类被用于定义`UserInfoForm`表单类的元数据。其中，model属性指定了与表单相关联的模型，这里是`UserInfo`模型。这意味着该表单将用于创建和更新`UserInfo`模型的实例。`fields`属性指定了要在表单中显示的字段列表。表单将显示`username`、`password`和`email`字段，用户可以填写这些字段的值。这些字段与`UserInfo`模型中的对应字段相关联。

#### 2.  定义校验规则

查找`Django`官方文档我们了解到`clean_filename` 方法是在表单子类上调用的—其中`filename`被替换为表单字段属性的名称。这个方法做任何特定属性的清理工作，与字段的类型无关。这个方法不传递任何参数。你需要在 self.cleaned_data 中查找字段的值，并且记住，此时它将是一个 Python 对象，而不是在表单中提交的原始字符串（它将在 cleaned_data 中，因为上面的一般字段 clean() 方法已经清理了一次数据）


于是我们对`username`、`password`、`email`制定相应的校验规则，添加到`UserRegistrationForm`类中去：

```python

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
```


#### 3. view建立

```python
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        email = form.data.get("email")
        code = form.data.get("emailcode")
        if not check_verification_code(email, code):
            return JsonResponse({'success': False, 'errors': "验证码错误"})  # 返回失败的 JSON 响应和表单错误信息
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # 返回成功的 JSON 响应
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # 返回失败的 JSON 响应和表单错误信息
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
```

**前端模板测试**

```html
{% block register-content %}
    <h2>注册您的信息</h2>
    <form method="post" id="registration-form">
        {% csrf_token %}
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="请输入用户名">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="请输入密码">
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">邮箱</label>
            <input type="text" class="form-control" id="email" placeholder="请输入您的邮箱" name="email">
        </div>
        <div class="mb-3">
            <label for="emailcode" class="form-label">验证码</label>
            <input type="text" class="form-control" id="emailcode" placeholder="请输入邮箱验证码" name="emailcode">
            <button type="button" class="btn btn-primary" id="sendButton">发送</button>
        </div>
        <button type="submit" class="btn btn-primary">注册</button>
    </form>


{% endblock %
```

`{% csrf_token %}`：这是Django模板标签，用于生成和包含CSRF令牌。CSRF令牌用于防止跨站请求伪造攻击。

`注意：本次前端采用的说Bootstrap5`

#### 4. 路由注册

```python
path('user-info/register', views.register, name='register'),
```



#### 5. 功能测试

1. **界面展示**

![](./images/3-register.png)

2. **注册成功**

- `username`:`3210561027`
- `password`:`3210561027`
- `email`:`854978151@qq.com`

![](./images/3-register-successfully.png)


3. **注册失败**

再次使用上面相同的用户名

![](./images/3-register-fail.png)

**注：所有的css代码见附件**



### 3.4. 用户登录功能

#### 1. 模型建立

和注册模块相同，我们也同样创建了一个`login-form`的模板，代码如下所示:

```python
class UserLoginForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    
     class Meta:
        model = UserInfo
        fields = ['username', 'password']
```

#### 2. 定义校验规则

```python
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

```

1. 首先，`clean`调用父类的`clean`方法，以获取经过默认验证的表单数据。

2. 然后，它从清理后的数据中获取`username`和`password`的值。

3. 如果`username`和`password`都存在，它执行以下验证逻辑：

   - 首先，它尝试通过`UserInfo.objects.get(username=username)`查询数据库获取与输入的`username`相匹配的用户对象。

   - 如果查询到了用户对象，它会进一步检查以下条件：

     - 用户名为空字符串 (`user.username == ""`)，或者
     - 密码不匹配 (`user.password != password`)。

     如果任何一个条件不满足，它会抛出一个`forms.ValidationError`异常，提示用户名或密码无效。否则，它将用户对象的`user_id`值存储到清理后的数据中(`cleaned_data['user_id']`)。

4. 如果查询数据库时捕获到`UserInfo.DoesNotExist`异常，它会抛出一个`forms.ValidationError`异常，提示用户名或密码无效。

5. 最后，它返回清理后的数据`cleaned_data`。

该`clean`方法的目的是在验证表单数据时，检查用户名和密码的有效性，并将验证通过的用户ID存储到清理后的数据中。

#### 3. view建立

```python	
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            user_name = form.cleaned_data.get('username')
            token = serializer.dumps({'user_id': user_id, 'username': user_name})
            return JsonResponse({'success': True, 'token': token})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form}
```

1. 首先，检查请求的方法是否为POST。如果是POST请求，表示用户提交了登录表单。
2. 创建一个`UserLoginForm`实例，使用请求中的POST数据初始化表单。
3. 调用`is_valid()`方法验证表单数据。如果表单数据有效，则执行以下操作：
   - 从清理后的数据中获取`user_id`和`username`的值。
   - 使用`serializer`对用户ID和用户名进行序列化，生成一个令牌(token)。
   - 返回一个JSON响应，包含登录成功的标志(`success=True`)和生成的令牌(`token`)。
4. 如果表单数据无效，则执行以下操作：
   - 使用`errors.as_json()`方法将表单的错误信息转换为JSON格式。
   - 返回一个JSON响应，包含登录失败的标志(`success=False`)和表单的错误信息(`errors`)。
5. 如果请求的方法不是POST，表示是首次加载登录页面，创建一个`UserLoginForm`实例。
6. 渲染登录页面模板`login.html`，将表单实例传递给模板，以便在页面中显示表单。

**登录模板**

```html	
 <form method="post" id="login-form">
        {% csrf_token %}
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input type="text" class="form-control" id="username" name="username" placeholder="请输入用户名">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="请输入密码">
        </div>
        <button type="submit" class="btn btn-primary">登录</button>
    </form>
```



#### 4. 路由注册

```python
  path('user-info/login', views.login_view, name='login'),
```

#### 5. 功能测试

```js
 $('#login-form').submit(function (event) {
                event.preventDefault(); // 阻止表单默认提交
                // 发起 Ajax 请求
                $.ajax({
                    url: '{% url 'login' %}',  // 登录处理视图的 URL
                    type: 'POST',
                    data: $(this).serialize(),  // 序列化表单数据
                    success: function (response) {
                        if (response.success) {
                            // 登录成功
                            let user = {
                                username: $("#username").val(),
                                token:response.token
                            };
                            localStorage.setItem('user', JSON.stringify(user));
                            // 调用修改函数


                            showAlert('success', 'Login successful!' + '  1.5s后跳转到主页');
                            {#$(' #login-form').hide()#}
                            // 延时 3 秒后执行回调函数
                            setTimeout(function () {
                                window.location.href = '{% url 'home' %}';  // 重定向到成功页面
                            }, 1500);  // 延时时间为 3000 毫秒，即 3 秒
                        } else {
                            // 登录失败
                            showAlert('danger', 'Login failed. Please check your credentials.');
                        }
                    },
                    error: function (response) {
                        showAlert('danger', 'An error occurred during login.');  // 处理请求错误
                    }
                });
            });
```



![](./images/4-logins.png)

![](./images/4-login2.png)

### 3.5. 用户修改密码

#### 1. 模型建立

```python
class ModifyUserPassword(forms.ModelForm):
    username = forms.CharField()
    old_password = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)
    
        class Meta:
        model = UserInfo
        fields = ['username', 'password']
```

#### 2. 定义校验规则

```python
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
```

1. 首先，从`cleaned_data`属性中获取表单字段的值，包括`username`、`old_password`、`password`和`confirm_password`。
2. 检查`password`和`confirm_password`是否相等，如果不相等，则抛出`forms.ValidationError`异常，提示两次密码不匹配。
3. 如果`username`、`old_password`和`password`都有值，执行以下操作：
   - 尝试根据`username`获取`UserInfo`对象。
   - 检查获取到的用户对象的`username`和`old_password`是否与表单字段的值匹配，如果不匹配，则抛出`forms.ValidationError`异常，提示用户不能存，不能修改。
   - 检查获取到的用户对象的`password`是否与`old_password`匹配，如果不匹配，则抛出`forms.ValidationError`异常，提示原密码错误。
   - 更新用户对象的`password`字段为新的`password`值。
4. 如果根据`username`未找到对应的`UserInfo`对象，抛出`forms.ValidationError`异常，提示用户不存在，不能修改。

#### 3. view建立

```python
def modifyPassword(request, username):
    if request.method == 'POST':
        form = ModifyUserPassword(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            print(errors)
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ModifyUserPassword()
    return render(request, 'modify_password.html', {'form': form}
```

**修改模板**

```html
{% block modify-user-password %}
    <form method="post" id="modify-password-form">
        {% csrf_token %}
        <div class="mb-3">
            <input type="hidden" class="form-control" id="username" name="username" placeholder="请输入用户名" >
        </div>
        <div class="mb-3">
            <label for="old_password" class="form-label">old_password</label>
            <input type="password" class="form-control" id="old_password" name="old_password" placeholder="请输入旧的密码">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" name="password" placeholder="请输入新的密码">
        </div>
        <div class="mb-3">
            <label for="confirm_password" class="form-label">confirm_Password</label>
            <input type="password" class="form-control" id="confirm_password" name="confirm_password" placeholder="请确认新的密码">
        </div>
        <button type="submit" class="btn btn-primary">提交修改</button>
    </form>
{% endblock %
```

#### 4. 路由注册

```python
    path('modify-password', views.modifyPassword, name='modify-password'),
```

#### 5. 功能测试

**将用户`3210561027`的密码修改为`12345678`**

**修改前**

```shell
mysql> select password from userInfo_userinfo where username='3210561027';
+------------+
| password   |
+------------+
| 3210561027 |
+------------+
1 row in set (0.09 sec)
```

![](./images/5-modify.png)

**修改后**

```shell
mysql> select password from userInfo_userinfo where username='3210561027';
+----------+
| password |
+----------+
| 12345678 |
+----------+
1 row in set (0.10 sec)
```

#### 3.6. 用户重置密码

#### 1. 模型建立

```python
class ResetPassword(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    code = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)
    
    class Meta:
        model = UserInfo
        fields = ['username', 'password']
```

- - `username`：字符型字段，用于输入用户名，最大长度为255个字符。
  - `email`：字符型字段，用于输入邮箱地址，最大长度为255个字符。
  - `code`：字符型字段，用于输入验证码，最大长度为255个字符。
  - `password`：字符型字段，用于输入新密码，最大长度为255个字符。
  - `confirm_password`：字符型字段，用于再次输入新密码进行确认，最大长度为255个字符。
- `Meta`内部类指定了该表单所基于的模型类为`UserInfo`，并指定了需要包含的字段为`username`和`password`。

#### 2. 定义校验规则

**该规则同上，不在赘述**

```python
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
```

- 在`clean`方法中，首先通过`self.cleaned_data.get()`方法获取表单字段的值，包括`username`、`password`、`email`、`code`和`confirm_password`。
- 然后进行一系列的验证逻辑：
  - 验证密码和确认密码是否匹配，如果不匹配，则抛出`forms.ValidationError`异常，提示密码不匹配。
  - 如果存在用户名和密码，通过`UserInfo.objects.get()`方法尝试获取用户对象。
  - 验证验证码的正确性，使用`check_verification_code`函数来检查验证码是否正确，如果不正确，则抛出`forms.ValidationError`异常，提示验证码错误。
  - 验证用户名的匹配性，如果表单中的用户名和获取到的用户对象的用户名不一致，则抛出`forms.ValidationError`异常，提示用户不能修改。
- 如果在验证过程中捕获到`UserInfo.DoesNotExist`异常，说明用户不存在，抛出`forms.ValidationError`异常，提示用户不存在，不能修改。
- 如果验证通过，使用`UserInfo.objects.filter().update()`方法更新用户对象的密码。

#### 3. view建立

```python
def resetPassword(request):
    if request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ResetPassword()
    return render(request, 'rest_password.html', {'form': form})
```

#### 4. 路由注册

```python
    path('reset-password',views.resetPassword,name='reset-password'),
```

#### 5. 功能测试

**重置之前**

```shell
mysql> select password from userInfo_userinfo where username='3210561027';
+----------+
| password |
+----------+
| 12345678 |
+----------+
1 row in set (0.10 sec)
```

![](./images/6-reset.png)

**重置之后**

```python
mysql> select password from userInfo_userinfo where username='3210561027';
+-----------+
| password  |
+-----------+
| 147852369 |
+-----------+
1 row in set (0.11 sec)
```

### 3.6. 鉴权中间件

我们需要将某些功能对用户进行限制，比如，修改密码必须在登录之后等等，于是我们制作了一个鉴权中间件，保证用户登录的情况下才能使用相关的功能。

```python
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('token')  # 获取请求中的 token（假设存储在 Cookie 中）

        if not token:
            # 如果没有 token，用户未登录，重定向到登录页面或其他适当的处理方式
            return redirect('login')  # 登录页面的URL名称

        try:
            # 创建反序列化器，使用与生成 token 相同的密钥
            data = serializer.loads(token)  # 解析 token

            user_id = data.get('user_id')
            username = data.get('username')
            if user_id is None or username is None:
                return redirect('login')  # 登录页面的URL名称

            # 将 user_id 和 username 添加到 kwargs 中，传递给视图函数
            # kwargs['user_id'] = user_id
            kwargs['username'] = username

        except BadSignature:
            # token 无效，用户未登录，重定向到登录页面或其他适当的处理方式
            return redirect('login')  # 登录页面的URL名称

        return view_func(request, *args, **kwargs)

    return wrappe
```

- `login_required`是一个装饰器函数，它接受一个视图函数`view_func`作为参数，并返回一个新的包装函数`wrapper`。
- 在`wrapper`函数中，首先尝试从请求的Cookie中获取名为`token`的值，即用户的身份认证令牌。
- 如果没有获取到`token`，说明用户未登录，可以根据具体需求进行处理，例如重定向到登录页面或其他适当的操作。
- 如果成功获取到`token`，则使用与生成令牌时相同的密钥进行反序列化，将令牌解析为原始数据。
- 解析出`user_id`和`username`，如果其中任一值为`None`，说明令牌无效或不完整，可以根据具体需求进行处理，例如重定向到登录页面或其他适当的操作。
- 如果成功解析出`user_id`和`username`，则将它们添加到`kwargs`中，传递给原始的视图函数。
- 如果解析过程中捕获到`BadSignature`异常，说明令牌无效或被篡改，可以根据具体需求进行处理，例如重定向到登录页面或其他适当的操作。
- 最后，返回原始的视图函数`view_func`，并传递请求和其他参数。

当用户没有登陆时，访问相关的服务时，会自动跳转到登录页面，保证了系统的安全性。

## 4. 用户建议模型

### 4.1. 模型介绍

```python
class UserSuggest(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.subject
```

`UserSuggest`是一个Django模型，用于存储用户建议信息。下面是对该模型的简要介绍：

- `username`是一个字符型字段，用于存储用户的用户名，其最大长度为255个字符。
- `email`是一个字符型字段，用于存储用户的电子邮件地址，其最大长度为255个字符。
- `subject`是一个字符型字段，用于存储建议的主题，其最大长度为255个字符。
- `text`是一个文本型字段，用于存储建议的具体内容。

### 4.2. 建议功能

#### 1. 模型建立

```python
class UserSuggestForm(forms.ModelForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserSuggest
        fields = ['username', 'email', 'subject', 'text']
```

#### 2. 定义校验规则

```python
 def clean_username(self):
        username = self.cleaned_data.get('username')
        # 自定义校验规则
        if len(username) < 5:
            raise forms.ValidationError("用户名长度不能少于5个字符")
        return username
```

#### 3. view建立

```python
@login_required
def contact(request, username):
    if request.method == 'POST':
        form = UserSuggestForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})  # 重定向到成功页面
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UserSuggestForm()
    return render(request, 'contact.html', {'form': form}
```

#### 4. 路由注册

```python
  path('contact', views.contact, name='contact'),
```

#### 5. 功能测试

**测试之前**

```shell
mysql> select * from userInfo_usersuggest where username='3210561027';
Empty set
```

![](./images/7-su.png)

```shell
mysql> select * from userInfo_usersuggest where username='3210561027';
+----+------------+------------------+--------------+----------------+
| id | username   | email            | subject      | text           |
+----+------------+------------------+--------------+----------------+
|  6 | 3210561027 | 854978151@qq.com | test-suggest | 这是测试的主题 |
+----+------------+------------------+--------------+----------------+
1 row in set (0.14 sec)

```

## 5. 账单模型

### 5.1. 模型介绍

```python
class UserBar(models.Model):
    username = models.CharField(max_length=255)
    bar = models.BigIntegerField()
    # 添加其他字段...

    class Meta:
        db_table = 'bars'
```

- `username`是一个字符型字段，用于存储用户的用户名，其最大长度为255个字符。
- `bar`是一个大整型字段，用于存储柱用户所使用数据的字节数。

### 5.1. 账单显示功能

#### 1. Django过滤器

```python
# custom_filters.py

from django import template

register = template.Library()


@register.filter
def divide(value, divisor):
    return round(int(value) / divisor, 2)

```

- `divide`函数接受两个参数：`value`和`divisor`，表示被除数和除数。
- 在函数体内，它执行整数除法运算，并使用`round`函数将结果保留两位小数。
- 最后，函数返回运算结果。

#### 2. Bars 模板

```html
{% extends 'base.html' %}
{% load  custom_filters %}
{% block form-bar %}
    <table class="table table-info  table-striped table-hover table-bordered">
        <thead>
        <tr>
            <th scope="col">ID</th>
            <th scope="col">Username</th>
            <th scope="col">Bars</th>
        </tr>
        </thead>
        <tbody>
        {% for bar in bars %}
            <tr>
                <th scope="row">1</th>
                <td>{{ bar.username }}</td>
                <td>{{ bar.bar|divide:65536 }} MB</td>

            </tr>
        {% endfor %}

        </tbody>
    </table>
{% endblock %}

```

- 在`{% block form-bar %}`和`{% endblock %}`之间的部分定义了一个表格，用于展示用户使用数据量。
- 使用`{% for bar in bars %}`指令迭代遍历一个名为`bars`的变量（可能是从视图传递过来的上下文中获取的），每个`bar`代表一个bars对象。
- 在表格的每一行中，使用`{{ bar.username }}`和`{{ bar.bar|divide:65536 }} MB`显示属性。`{{ bar.bar|divide:65536 }}`使用了刚刚定义的自定义过滤器`divide`进行除法运算，并显示结果为MB单位的值。
- 最后，使用`{% endfor %}`结束`{% for %}`循环。

#### 3. view 建立

```python
@login_required
def bar_list(request, username):
    bars = UserBar.objects.filter(username=username)
    return render(request, 'bars.html', {'bars': bars})
```

#### 4. 路由注册

```python
   path('bars', views.bar_list, name='bars'),
```

#### 5. 功能测试

**分别使用`admin`和`3210561027`两个账户测试结果**

```shell
mysql> select * from bars where username in ('admin','3210561027');
+----+----------+------------+
| id | bar      | username   |
+----+----------+------------+
|  1 | 10870288 | admin      |
|  2 |  4486264 | 3210561027 |
+----+----------+------------+
```

![](./images/8-bars1.png)

![](./images/8-bars2.png)
