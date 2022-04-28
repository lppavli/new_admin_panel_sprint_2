from django.urls import path, include
from rest_framework import routers

from movies.api.v1 import views
from movies.api.v1.views import MovieViewSet

router = routers.DefaultRouter()
router.register(r"movies", MovieViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('movies/', views.MovieViewSet.as_view()),
    # path('movies/<uuid:pk>/', views.MovieAPIList.as_view()),
]