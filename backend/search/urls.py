from django.urls import path

from .views import AlgoliaSearchListView


urlpatterns = [
    path('', AlgoliaSearchListView.as_view(), name='search')
]
