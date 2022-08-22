from rest_framework import generics, permissions
from .models import Rating
from .serializers import RatingSerializer
from drf_api_cutback.permissions import IsOwnerOrReadOnly

class RatingsList(generics.ListCreateAPIView):
    """
    List all Ratings.
    Authenticated users can create new Rating instances.
    """

    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Rating.objects.all()

class RatingDetail(generics.RetrieveDestroyAPIView):
    """
    Retrive a specific Rating.
    The owner of the Raging can delete it from the database.
    """
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsOwnerOrReadOnly]