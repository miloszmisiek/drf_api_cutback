from rest_framework import generics, filters, status
from rest_framework.response import Response
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
        'in_stock',
        'category',
        'brand',
        'country',
        'city'

    ]
    ordering_fields = [
        'price',
        'avg_score',
        'all_scores',
        'title',
        'created_at',
        'country'
    ]

    search_fields = [
        'owner__username',
        'title',
        'description',
        'street',
        'city',
        'country'
    ]


class ProductImages(generics.ListCreateAPIView):
    """
    List all Products images.
    Authenticated users can create new instances of Products images.
    """
    
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductImage.objects.all()

    def perform_create(self, serializer):
        """
        Saves owner as a current user.
        """
        serializer.save(owner=self.request.user)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List specific Product by it's id.
    The owner of the Product instance can update or
    delete the product from the database.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()


class ProductImagesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List specific Product image by it's id.
    The owner of the Product image instance can update or
    delete the product from the database.
    """
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = ProductImage.objects.all()


class ProductChoicesView(generics.GenericAPIView):
    """
    List categories and currencies choices for Product model.
    """

    def append_key_value_pairs(self, choices):
        """
        Iterate over choices and return list of choice's objects
        """
        return_list = []
        for i in choices:
            key, value = i
            obj = {"key": key, "value": value}
            return_list.append(obj)
        return return_list

    def get(self, request):
        try:
            return_dict = {
                "CATEGORIES": self.append_key_value_pairs(Product.CATEGORIES),
                "CURRENCIES": self.append_key_value_pairs(Product.CURRENCY_CHOICES),
            }
            return Response(return_dict, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Empty or invalid categories choices"}, status=status.HTTP_400_BAD_REQUEST)
