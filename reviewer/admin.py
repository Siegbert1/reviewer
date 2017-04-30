from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Card, User, Progress, Category
# Register your models here.
admin.site.register(Card)
admin.site.register(User, UserAdmin)
admin.site.register(Category)




# needed because in models.py Progress.lasttime is set to auto_now and wouldnt display by default
class ProgressAdmin(admin.ModelAdmin):
    readonly_fields = ('lasttime',)
admin.site.register(Progress, ProgressAdmin)
