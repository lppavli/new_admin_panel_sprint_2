from rest_framework import serializers

from ...models import Filmwork


class MovieSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    class Meta:
        model = Filmwork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'persons'
        )
