from django.contrib import admin
from .models import Profile, Category, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name',)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('category', 'author', 'title', 'content', 'publish_date')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
