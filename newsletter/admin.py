from django.contrib import admin
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'department', 'created_at', 'is_approved', 'is_published')  # Include department
    list_filter = ('is_approved', 'is_published', 'created_at', 'category')
    search_fields = ('title', 'content', 'author__username', 'category__name')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
