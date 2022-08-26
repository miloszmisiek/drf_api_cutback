from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import IntegrityError
from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serilizer for Rating model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    product_name = serializers.ReadOnlyField(source='product.title')
    created_at = serializers.SerializerMethodField()

    def create(self, validated_data):
        # to avoid crashing server with 500 error
        try:
            return super().create(validated_data) # super() because we are refering to method from ModelSerializer
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    class Meta:
        model = Rating
        fields = ('id', 'owner', 'product','product_name', 'score', 'created_at',)