from django.urls import path
from .views import TourListCreateView, TourRetrieveUpdateDestroyView

urlpatterns = [
    path('', TourListCreateView.as_view(), name='tour-list-create'),
    path('<int:pk>/', TourRetrieveUpdateDestroyView.as_view(), name='tour-detail'),
]