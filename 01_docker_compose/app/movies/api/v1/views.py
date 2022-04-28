from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import viewsets

from .serializers import MovieSerializer
from movies.models import Filmwork


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Filmwork.objects.prefetch_related().all().values().annotate(
        genres=ArrayAgg("genres__name", distinct=True)).annotate(
        directors=ArrayAgg("persons__full_name", distinct=True,
                           filter=Q(personfilmwork__role="director"))).annotate(
        writers=ArrayAgg("persons__full_name", distinct=True,
                         filter=Q(personfilmwork__role="writer"))).annotate(
        actors=ArrayAgg("persons__full_name", distinct=True,
                        filter=Q(personfilmwork__role="actor")))
    serializer_class = MovieSerializer
