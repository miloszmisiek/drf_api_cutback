from django.db.models import Count
from rest_framework import generics, filters #, permissions
# from django_filters.rest_framework import DjangoFilterBackend #third-party library django-filter
from .models import Profile
from .serializers import ProfileSerializer
from drf_api_cutback.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()