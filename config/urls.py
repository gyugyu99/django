# config/urls.py

from django.contrib import admin
from django.urls import path

from todo.views import todo_list, todo_info # 추가


urlpatterns = [
		path('admin/', admin.site.urls),
    path('todo/', todo_list, name='todo_list'), # 추가
    path('todo/<int:todo_id>/', todo_info, name='todo_info'), #추가
]
