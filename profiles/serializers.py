from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    email = serializers.EmailField(source='owner.email')
    first_name = serializers.CharField(source='owner.first_name')
    last_name = serializers.CharField(source='owner.last_name')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'email', 'first_name', 'last_name',
            'phone_number', 'image', 'created_at', 'updated_at',
            'is_owner',
        ]

    def update(self, instance, validated_data):
        """
        Custom Update method to handle sourced fields in Profile serializer
        """
        # saving User instances
        owner_data = validated_data.pop('owner')
        owner = instance.owner
        for k,v in owner_data.items():
            setattr(owner, k, v)
        owner.save()
        #saving Profile instances
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        return instance