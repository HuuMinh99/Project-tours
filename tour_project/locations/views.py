# locations/views.py

from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Location
from .serializers import LocationSerializer

class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all().order_by('-created_at')
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
