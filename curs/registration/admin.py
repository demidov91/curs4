from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from lucenequerybuilder import Q


from registration.utils import check_client
from forms import UserCustomAdminCreationForm, UserCustomAdminChangeForm
from models import Userprofile

import logging
logger = logging.getLogger(__name__)


    
class UserCustomAdmin(UserAdmin):
    '''
    Customize view email statistics
    '''
    list_display = ('username', 'is_staff', 'is_client')
    actions = UserAdmin.actions + ['set_client', 'unset_client']
     
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    def is_client(self, obj):
        return check_client(obj)

    def set_client(modeladmin, request, queryset):
        for user in queryset:
            if not user.is_staff:
                profile = Userprofile.index.get(username=user.username)
                profile.set_is_client(True)
                
                
    def unset_client(modeladmin, request, queryset):
        for user in queryset:
            if not user.is_staff:
                profile = Userprofile.index.get(username=user.username)
                profile.set_is_client(False)                
        

    is_client.boolean = True
    add_form = UserCustomAdminCreationForm
    form = UserCustomAdminChangeForm

admin.site.unregister(User)
admin.site.register(User, UserCustomAdmin)