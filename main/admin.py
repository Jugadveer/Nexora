from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Project, Position, Application
# Unregister the default User admin
admin.site.unregister(User)

# Register it again (optionally with custom admin)
admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Position)
admin.site.register(Application)