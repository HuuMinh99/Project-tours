from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Tour
from .serializers import TourSerializer

class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all().order_by('-id')
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']  # ✅ tìm kiếm theo title

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class TourRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]