import logging
import requests
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings

from task.models import Movie, Comment, Top
from task.serializers import MovieSerializer, CommentSerializer, TopSerializer


fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request):
        data = self.get_movie_details(request.data)
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

    @staticmethod
    def get_movie_details(data):
        movie_json = requests.get(f"https://omdbapi.com/?t={data['title']}&apikey=8e68ddd9").json()
        data._mutable = True
        data['title'] = movie_json['Title']
        data['year'] = movie_json['Year'][:4]
        data['imdb_id'] = movie_json['imdbID']
        data['type'] = movie_json['Type']
        data['poster'] = movie_json['Poster']
        return data


class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['movie__id']

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class TopListView(APIView):

    def get(self, request):
        data = self.count_top()
        serializer = TopSerializer(data=data, many=True)
        if serializer.is_valid():
            response = Response(serializer.data)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


    def post(self, request):
        data = self.count_top(request.data)
        serializer = TopSerializer(data=data, many=True)
        if serializer.is_valid():
            response = Response(serializer.data)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


    @staticmethod
    def count_top(data=None):
        top = []
        movies = Movie.objects.all()
        if data:
            if data['date_start']:
                movies = movies.filter(comment__date__gte=data['date_start'])
            if data['date_end']:
                movies = movies.filter(comment__date__lte=data['date_end'])
        for movie in movies.distinct():
            comment = Comment.objects.filter(movie=movie)
            if data:
                if data['date_start']:
                    comment = comment.filter(date__gte=data['date_start'])
                if data['date_end']:
                    comment = comment.filter(date__lte=data['date_end'])
            top.append({
                'movie_id': movie.id,
                'total_comments': len(comment),
                'rank': 0
            })
        top = sorted(top, key=lambda x: x['total_comments'], reverse=True)
        position = 1
        for x in range(len(top)):
            if x == 0:
                if top[x]['total_comments'] != 0:
                    top[0]['rank'] = position
            else:
                if top[x]['total_comments'] == top[x-1]['total_comments']:
                    top[x]['rank'] = position
                else:
                    position += 1
                    if position == 4:
                        break
                    top[x]['rank'] = position
        new_top = []
        for movie in top:
            if movie['rank'] != 0 and movie['total_comments'] != 0:
                new_top.append(movie)
        return new_top
