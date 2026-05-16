from rest_framework import serializers
from .models import Resource, Booking
from django.contrib.auth.models import User

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ["id", "name", "description", "capacity", "has_air_conditioner"]
        
class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = ["id", "user", "resource", "start_time", "end_time", "time"]
        read_only_fields = ["user"]
        
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user