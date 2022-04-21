import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=30, choices=Type.choices)
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film')
        verbose_name_plural = _('Films')


class GenreFilmwork(models.Model):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of filmwork')
        verbose_name_plural = _('Genres of filmwork')
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]
        constraints = [
            UniqueConstraint(fields=['film_work_id', 'genre_id'], name='film_work_genre'),
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class PersonFilmWork(models.Model):
    class Role(models.TextChoices):
        DIRECTOR = 'director', _('Director')
        WRITER = 'writer', _('Writer')
        ACTOR = 'actor', _('actor')
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(max_length=10,
                            choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person of filmwork')
        verbose_name_plural = _('Persons of filmwork')
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
        constraints = [
            UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role'),
        ]
