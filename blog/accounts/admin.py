from django.contrib import admin
from .models import *

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_verified']

admin.site.register(Author)
admin.site.register(Client, ClientAdmin)
admin.site.register(Genders)