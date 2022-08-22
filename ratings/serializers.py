from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    product_name = serializers.ReadOnlyField(source='product_rating.title')
    class Meta:
        model = Rating
        fields = ('id', 'owner' 'product','product_name', 'score', 'created_at' )