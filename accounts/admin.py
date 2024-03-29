from django.contrib import admin
from django.contrib.admin.decorators import display
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import Account, UserProfile
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'last_login', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    list_editable = ('is_active', )
    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self, object):
#         return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
#     thumbnail.short_description = 'Profile Picture'
#     list_display = ('thumbnail', 'user', 'city', 'state', 'country')


admin.site.register(Account, AccountAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
