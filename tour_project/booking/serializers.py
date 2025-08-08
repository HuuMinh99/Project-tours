from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ['id', 'user', 'total_price', 'booking_date']
        fields = '__all__'

    def create(self, validated_data):
        # Tự tính total_price
        tour = validated_data['tour']
        quantity = validated_data['quantity']
        validated_data['total_price'] = tour.price * quantity
        return super().create(validated_data)
