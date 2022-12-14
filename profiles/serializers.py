from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    email = serializers.ReadOnlyField(source='owner.email')
    first_name = serializers.CharField(source='owner.first_name')
    last_name = serializers.CharField(source='owner.last_name')
    is_owner = serializers.SerializerMethodField()
    products_count = serializers.ReadOnlyField()
    ratings_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    avg_score = serializers.SerializerMethodField()
    all_scores = serializers.SerializerMethodField()



    def get_is_owner(self, obj):
        """
        Method checks if the current user is the owner of the profile
        and returns boolean value.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_avg_score(self, obj):
        """
        Method returns avg_score if any or 0
        """
        return Profile.objects.get(pk=obj.id).avg_score if Profile.objects.get(pk=obj.id).avg_score else 0

    def get_all_scores(self, obj):
        """
        Method returns all_scores if any or 0
        """
        return Profile.objects.get(pk=obj.id).all_scores if Profile.objects.get(pk=obj.id).all_scores else 0

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'email', 'first_name', 'last_name',
            'phone_number', 'image', 'created_at', 'updated_at',
            'is_owner', 'products_count', 'ratings_count', 'comments_count', 'avg_score', 'all_scores'
        ]

    def update(self, instance, validated_data):
        """
        Custom Update method to handle sourced fields in Profile serializer
        """
        # saving User instances
        owner_data = validated_data.pop('owner')
        owner = instance.owner
        for k, v in owner_data.items():
            setattr(owner, k, v)
        owner.save()
        # saving Profile instances
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance
