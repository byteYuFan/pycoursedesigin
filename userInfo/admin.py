from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserInfo, UserSuggest,UserBar


#
# admin.site.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'flag', 'time')
    search_fields = ('username', 'email')
    list_filter = ('flag', 'time')


admin.site.register(UserInfo, UserInfoAdmin)

admin.site.register(UserSuggest)

admin.site.register(UserBar)
