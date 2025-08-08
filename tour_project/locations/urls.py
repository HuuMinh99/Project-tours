# locations/urls.py

from django.urls import path
from .views import (
    LocationListCreateView,
    LocationRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', LocationListCreateView.as_view(), name='location-list-create'),
    path('<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),
]
