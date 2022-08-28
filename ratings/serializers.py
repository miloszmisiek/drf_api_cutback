from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import IntegrityError
from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serilizer for Rating model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    product_name = serializers.ReadOnlyField(source='product.title')
    created_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Method checks if the current user is the owner of the profile and returns boolean value.
        """
        request = self.context['request']
        return request.user == obj.owner

    def create(self, validated_data):
        """
        Custom create method to avoid crashing server with 500 error.
        """
        try:
            # super() because we are refering to method from ModelSerializer
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })

    def get_created_at(self, obj):
        """
        Returns instance's created_at field as naturaltime format.
        """
        return naturaltime(obj.created_at)

    class Meta:
        model = Rating
        fields = (
            'id', 'owner', 'is_owner',
            'product', 'product_name',
            'score', 'created_at',
        )
