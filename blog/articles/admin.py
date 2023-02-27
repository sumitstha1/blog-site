from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)

class ArticleImageAdmin(admin.StackedInline):
    model = ArticleImage

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_latest', 'is_approved', 'created_at', 'updated_at']
    inlines = [ArticleImageAdmin]

admin.site.register(Articles, ArticleAdmin)