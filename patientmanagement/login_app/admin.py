from django.contrib import admin
from login_app.models import User
from login_app.models import Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)

