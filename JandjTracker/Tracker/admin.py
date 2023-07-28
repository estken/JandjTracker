from django.contrib import admin
from .models import *
from .user_model import ClientUser
from django.contrib.auth.admin import UserAdmin
from .job_history_model import JobHistory
from .payments_model import PaymentsModel
from .log_history_model import LogHistoryModel
# Register your models here.

class UserAdminConfig(UserAdmin):
    # Admin can either search with email address or with username.
    search_fields = ('email', 'username')
    # arrange the record in descending order of date joined.
    ordering = ('-date_joined',)
    # change the display of the user
    list_display = ('email','name','username', 'date_joined', 'is_staff','is_active', 'is_changed',)
    # Arrange the fields in nice partitions.
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_changed')}),
        ('Personal',{'fields': ('name','date_joined', 'last_login',)}),
    )

    # These are the fields we want displayed on the admin page whenever we want to create a new user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'email', 'username', 'name','password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_changed'),}
        ),
    )

register = admin.site.register
register(ClientUser, UserAdminConfig)
# Register your models here.

admin.site.register(JobsModel)
admin.site.register(JobHistory)
admin.site.register(PaymentsModel)
admin.site.register(LogHistoryModel)
