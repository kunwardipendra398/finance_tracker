from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Register Profile model
admin.site.register(Profile)

# Optional: Show Profile inline with User in Admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

# Unregister default User admin and register new one with Profile inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)