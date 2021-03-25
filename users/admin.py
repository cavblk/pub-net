from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import AuthUser


# Register your models here.
@admin.register(AuthUser)
class AuthUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'profile_avatar')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email', 'profile__avatar')

    def profile_avatar(self, instance):
        return instance.profile.avatar
    profile_avatar.short_description = 'Profile Avatar'


class MyClass:
    def __init__(self, x):
        self.a = x


print(MyClass(7).a)
print(7 or 3 + 8)
