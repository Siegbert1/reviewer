from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Card, User, Progress
# Register your models here.
admin.site.register(Card)
admin.site.register(Progress)
admin.site.register(User, UserAdmin)
