# core/serializers.py
from rest_framework import serializers
from .models import Restaurant, Package, Cuisine

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ['id', 'name']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'price', 'duration', 'description', 'image']

class RestaurantSerializer(serializers.ModelSerializer):
    cuisines = serializers.PrimaryKeyRelatedField(
        queryset=Cuisine.objects.all(),
        many=True,
        required=False  # Make optional if not always required
    )
    package = PackageSerializer()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'phone', 'manager_name', 'manager_phone', 'contact_email', 
                  'country', 'state', 'city', 'latitude', 'longitude', 'delivery_pickup', 
                  'cuisines', 'owner', 'package']

    def create(self, validated_data):
        cuisines_data = validated_data.pop('cuisines', [])
        package_data = validated_data.pop('package')
        package, created = Package.objects.get_or_create(**package_data)
        restaurant = Restaurant.objects.create(package=package, **validated_data)
        restaurant.cuisines.set(cuisines_data)  # Set the ManyToMany relationship
        return restaurant