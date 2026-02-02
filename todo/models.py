from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from sqlparse.sql import For


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #외래키를 설정한 후 on_delete 삭제 규칙 설(부모가 삭제되면 자식도 삭제)
    # CASCADE(종속), SET_NULL, PROTECT 옵션 .
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    # related_name은 역참조 옵션임
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)