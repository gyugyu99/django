# todo > admin.py

from django.contrib import admin
from todo.models import Todo, Comment


class CommentInline(admin.TabularInline):
    # admin.TabularInline을 상속하면 테이블(표)의 형태로 통합관리 UI보여줌
    model = Comment
    extra = 0
    fields = ('message', 'user')




@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_completed')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'user', 'message', 'created_at')
    list_filter = ('todo', 'user')
    search_fields = ('message', 'user')
    ordering = ('-created_at',)
    list_display_links = ('message',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'user', 'message')
        }),
    )
