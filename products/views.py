from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api_cutback.permissions import (
    IsOwnerOrReadOnly,
    IsAuthenticatedOrReadOnly
)
from .models import Product, ProductImage
from .serializers import ProductSerializer, ImageSerializer


class ProductList(generics.ListCreateAPIView):
    """
    List all Products.
    Authenticated users can create new instances of Products.
    Create method saves current user as owner.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        """
        Saves owner as a current user.
        """
        serializer.save(owner=self.request.user)

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = [
        'owner',
        'inStock',
        'category',
        'brand',
    ]
    ordering_fields = [
        'price',
        'avg_score',
        'all_scores',
        'title',
        'created_at',
    ]

    search_fields = [
        'owner__username',
        'title',
        'description'
    ]


class ProductImages(generics.ListCreateAPIView):
    """
    List all Products images.
    Authenticated users can create new instances of Products images.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductImage.objects.all()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List specific Product by it's id.
    The owner of the Product instance can update or
    delete the product from the database.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()
