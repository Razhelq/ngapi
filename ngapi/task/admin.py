from django.contrib import admin

from task.models import Movie, Comment


@admin.register(Movie)
class Movie(admin.ModelAdmin):
    list_display = ['title', 'year', 'type', 'imdb_id', 'poster']


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['movie', 'body']
