import requests
from task.models import Movie
from task.serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponse
import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

class MovieListView(APIView):

    def get(self, request, format=None):
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True, context={"request": request})
        response = Response(serializer.data)
        return response

    def post(self, request, format=None):
        data = self.look_for_movie(request.data)
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

    @staticmethod
    def look_for_movie(data):
        movie_json = requests.get(f"https://omdbapi.com/?t={data['title']}&apikey=8e68ddd9").json()
        data['title'] = movie_json['Title']
        data['year'] = movie_json['Year'][:4]
        data['imdb_id'] = movie_json['imdbID']
        data['type'] = movie_json['Type']
        data['poster'] = movie_json['Poster']
        return data


# class ProductView(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404
#
#     def get(self, request, id, format=None):
#         product = self.get_object(id)
#         serializer = ProductSerializer(product, context={"request": request})
#         response = Response(serializer.data)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def delete(self, request, id, format=None):
#         product = self.get_object(id)
#         product.delete()
#         response = Response(status=status.HTTP_204_NO_CONTENT)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def put(self, request, id, format=None):
#         product = self.get_object(id)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = Response(serializer.data)
#             Log.objects.create(request=request.get_full_path, response=response)
#             return response
#         response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def post(self, request, id, format=None):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = Response(serializer.data, status=status.HTTP_201_CREATED)
#             Log.objects.create(request=request.get_full_path, response=response)
#             return response
#         response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#
# class WrongEndpointView(APIView):
#
#     def get(self, request, format=None):
#         response = Http404
#         Log.objects.create(request=request.get_full_path, response=response)
#         raise Http404
#
#     def delete(self, request, format=None):
#         response = Response(status=status.HTTP_204_NO_CONTENT)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def put(self, request, format=None):
#         response = Response(status=status.HTTP_400_BAD_REQUEST)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def post(self, request, format=None):
#         response = Response(status=status.HTTP_400_BAD_REQUEST)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
#
#     def patch(self, request, format=None):
#         response = Response(status=status.HTTP_400_BAD_REQUEST)
#         Log.objects.create(request=request.get_full_path, response=response)
#         return response
