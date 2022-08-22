from django.db.models import Count
from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serilizer for Rating model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    product_name = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = Rating
        fields = ('id', 'owner', 'product','product_name', 'score', 'created_at',)