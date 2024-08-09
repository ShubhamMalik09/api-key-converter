from django.urls import path
from . import views

urlpatterns = [
    path('search', views.searchNews, name='search_news'),
]