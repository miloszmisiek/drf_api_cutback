from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Rating
from .serializers import RatingSerializer
from drf_api_cutback.permissions import (
    IsOwnerOrReadOnly,
    IsAuthenticatedOrReadOnly
)


class RatingsList(generics.ListCreateAPIView):
    """
    List all Ratings.
    Authenticated users can create new Rating instances.
    """

    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Rating.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'product',
        'owner'
    ]


class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrive a specific Rating.
    The owner of the Raging can delete it from the database.
    """
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
