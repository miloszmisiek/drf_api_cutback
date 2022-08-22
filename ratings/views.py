from django.db.models import Count
from rest_framework import generics, filters, permissions #, permissions
# from django_filters.rest_framework import DjangoFilterBackend #third-party library django-filter
from .models import Rating
from .serializers import RatingSerializer
from drf_api_cutback.permissions import IsOwnerOrReadOnly

class RatingsList(generics.ListCreateAPIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """

    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Rating.objects.all()

class RatingDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a follower
    No Update view, as we either follow or unfollow users
    Destroy a follower, i.e. unfollow someone if owner
    """
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsOwnerOrReadOnly]