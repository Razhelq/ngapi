from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=128, unique=True)
    year = models.PositiveIntegerField(null=True)
    type = models.CharField(max_length=128, null=True)
    imdb_id = models.CharField(max_length=32, unique=True, null=True)
    poster = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}'
