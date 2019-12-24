from django.contrib import admin

from members.models import User


@admin.register(User)
class User(admin.ModelAdmin):
    pass