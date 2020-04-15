from rest_framework import serializers
from task.models import Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("title", "year", "type", "imdb_id", "poster")
