from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import viewsets

from .serializers import MovieSerializer
from movies.models import Filmwork, Role


def aggredate_person(role):
    return ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role=role))


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Filmwork.objects.prefetch_related().all().values().annotate(
        genres=ArrayAgg("genres__name", distinct=True),
        directors=aggredate_person(role=Role.DIRECTOR),
        writers=aggredate_person(role=Role.WRITER),
        actors=aggredate_person(role=Role.ACTOR))
    serializer_class = MovieSerializer
