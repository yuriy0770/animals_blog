from django.contrib import admin
from main.models import Category, Post, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'background_image', 'views']
    list_filter = ['publish', 'created']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'publish'

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image_category', 'background_image')
        }),
        ('SEO и даты', {
            'fields': ('slug', 'publish', 'views'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'cat', 'is_published', 'publish', 'views', 'created', "slug"]
    list_display_links = ['title']
    list_filter = ['cat', 'is_published', 'publish', 'tags']
    search_fields = ['title', 'body', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'publish'
    readonly_fields = ['views', 'created', 'updated']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'name_animal', 'body', 'short_description', 'image', 'cat', 'tags')
        }),
        ('Публикация', {
            'fields': ('is_published', 'publish')
        }),
        ('SEO и статистика', {
            'fields': ('slug', 'views'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.short_description:
            obj.short_description = obj.body[:297] + '...' if len(obj.body) > 300 else obj.body
        super().save_model(request, obj, form, change)