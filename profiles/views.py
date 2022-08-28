from rest_framework import generics, filters
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from drf_api_cutback.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        products_count=Count('owner__product', distinct=True),
        ratings_count=Count('owner__rating', distinct=True),
        comments_count=Count('owner__comment', distinct=True)
    )

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        # list all profiles which owner's give rating to the selected product
        'owner__rating__product',
    ]
    ordering_fields = [
        'products_count',
        'ratings_count',
        'comments_count',
    ]

    search_fields = [
        'owner__username',
        'owner__first_name',
        'owner__last_name',
        'owner__email',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
