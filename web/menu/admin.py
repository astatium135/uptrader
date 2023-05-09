from django.contrib import admin

from .models import Menu

class MenuAdmin(admin.ModelAdmin):
    pass

admin.site.register(Menu, MenuAdmin)