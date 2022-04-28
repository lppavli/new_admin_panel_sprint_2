from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import BaseDetailView
from rest_framework import generics, viewsets

from .serializers import MovieSerializer
from movies.models import Filmwork


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Filmwork.objects.all()
    serializer_class = MovieSerializer

# class MoviesAPIList(generics.ListCreateAPIView):
#     queryset = Filmwork.objects.all()
#     serializer_class = MovieSerializer
#
#
# class MoviesApiView(generics.ListAPIView):
#     queryset = Filmwork.objects.all()[:10]
#     serializer_class = MovieSerializer

# class MoviesApiMixin:
#     model = Filmwork
#     http_method_names = ['get']
#
#     def get_queryset(self):
#         return Filmwork.objects.all()
#
#     def render_to_response(self, context, **response_kwargs):
#         return JsonResponse(context)
#
#
# class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = {
#             'results': list(self.get_queryset()),
#         }
#         return context
