from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api_cutback.permissions import IsOwnerOrReadOnly
from .models import Product, ProductImage
from .serializers import ProductSerializer, ImageSerializer

class ProductList(generics.ListCreateAPIView):
    """
    List all Products.
    Authenticated users can create new instances of Products.
    Create method saves current user as owner.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    # .annotate(**{f"score_count_{n}": Count('product_rating', filter=Q(product_rating__score=n), distinct=True) for n in range(len(Rating.RATE_CHOICES)+1)})
    # .annotate(
        # ratings_count=Count('product_rating', distinct=True),
        # score_avg=Avg('product_rating__score'),
    # ).order_by('-created_at')

    def perform_create(self, serializer):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductImage.objects.all()

    # def perform_create(self, serializer):
    #     print(self.request.image)
    #     # serializer.save(product=self.request.product)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    List specific Product by it's id.
    The owner of the Product instance can update or delete the product from the database.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Product.objects.all()
