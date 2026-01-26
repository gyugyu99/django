"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import render
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.urls import path
from django.shortcuts import render

movie_list = [
    {'title':'파묘', 'director':'정재원'},
    {'title':'두', 'director':'개'},
    {'title':'쫀', 'director':'노'},
    {'title':'쿠', 'director':'맛'}
]



def index(request):
    return HttpResponse('<h1>hello</h1>')

def book_list(request):

    # book_text = ''
    #
    # for i in range(0, 10):
    #     book_text += f'book {i}<br>'

    return render(request, 'book_list.html', {'range' : range(0, 10)})

def book(request, num):
    book_text = f'book {num}번 페이지 입니다'
    return HttpResponse(book_text)

def language(request, lang):
    return HttpResponse(f'<h1>{lang} 언어 페이지입니다.')

def python(request):
    return HttpResponse('python 페이지 입니다.')

def movies(request):
    # movie_titles = [movie['title'] for movie in movie_list]
    # response_text = ''
    #
    # for index, title in enumerate(movie_titles):
    #     response_text += f'<a href="/movie/{index}/">{title}</a><br>'

    return render(request, 'movies.html', {'movie_list':movie_list})

def movies_detail(request, index):
    if index > len(movie_list) -1:
        raise Http404

    movie = movie_list[index]

    return render(request, 'movie.html', {'movie':movie})


def gugu(request, num):
    context = {
        'num': num,
        'results': [(i, num * i)for i in range(1, 10)]
    }
    return render(request, 'gugu.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gugu/<int:num>/', gugu),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/<str:lang>', language),
    path('language/python/', python),
    path('movie/', movies),
    path('movie/<int:index>/', movies_detail),
    path('gugu/<int:num>/', gugu),
]
