from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from sqlparse.sql import For
from PIL import Image
from pathlib import Path
from io import BytesIO


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #외래키를 설정한 후 on_delete 삭제 규칙 설(부모가 삭제되면 자식도 삭제)
    # CASCADE(종속), SET_NULL, PROTECT 옵션 .
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    # 할 일(Todo)의 대표 썸네일 이미지를 저장하고 없으면 기본 이미지를 대신 보여줌
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails', default='todo/no_image/NO-IMAGE.gif', null=True, blank=True
    )
    # 할 일(Todo)가 완료되었을때 찍거나 업로드하는 인증 이미지
    completed_image = models.ImageField(upload_to='todo/completed_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # 데이터가 DB저장되기 전 장고는 save()를 호출하기 때문에 원본 저장시 썸네일 만들라고 추가 명령 내리기위해 save함수 정의
        if not self.completed_image:
            # 완료 이미지가 없으면 썸네일을 만들 이유가 없으니
            return super().save(*args, **kwargs)
            # 그냥 일반 저장 과정을 진행함

        image = Image.open(self.completed_image)
        # Pillow 라이브러리로 이미지 파일 개방
        image.thumbnail((100, 100))
        # 요구사항 썸네일 생성

        image_path = Path(self.completed_image.name)
        #파일 경로 분석 객체 생성

        thumbnail_name = image_path.stem
        #파일 이름만 ex) '.photo'
        thumbnail_extension = image_path.suffix
        #파일 확장자만 ex) '.jpg'
        thumbnail_filename = f'{thumbnail_name}_thumbnail{thumbnail_extension}'
        #최종 이름 photo_thumbnail.jpg 같은 형태로 조합


        # Pillow는 저장할 때 JPEG / PNG 같은 포멧 이름이 필요함
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        else:
            return super().save(*args, **kwargs)

        #파일을 하드디스크에 썼다가 다시 읽으면 속도가 느림 -> RAM(메모리) 공간을 임시로 빌려 처리
        temp_thumb = BytesIO()
        #메모리에 비어있는 가상 파일(버퍼)를 만듬
        image.save(temp_thumb, format=file_type)
        #썸네일 데이터를 이 가상 파일에 씀
        temp_thumb.seek(0)
        #데이터가 끝까지 써졌으니 읽기 위해 커스를 맨 앞으로 옮김

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        # 가상 파일 (temp_thump)에 담긴 내용을 thumbnail필드에 할당

        temp_thumb.close()
        #메로리 리소스 해제(청소)
        return super().save(*args, **kwargs)
        #모든 필드가 채워졌으니 DB에 저장


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    # related_name은 역참조 옵션임
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
