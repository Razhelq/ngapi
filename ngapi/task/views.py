import logging
import requests

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings

from task.models import Movie, Comment
from task.serializers import MovieSerializer, CommentSerializer


fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.DEBUG)

logging.basicConfig(format=fmt, level=lvl)
logging.debug("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))


class MovieListView(APIView):

    def get(self, request):
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True, context={"request": request})
        response = Response(serializer.data)
        return response

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

    # def get(self, request):
    #     search_fields = ['movie__id']
    #     filter_backends = (SearchFilter, )
    #     movie = Comment.objects.all()
    #     serializer = CommentSerializer(movie, many=True, context={"request": request})
    #     response = Response(serializer.data)
    #     return response
    #
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


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
