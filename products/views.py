from rest_framework import generics, permissions
from drf_api_cutback.permissions import IsOwnerOrReadOnly
from .models import Product, ProductImage
from .serializers import ProductSerializer, ImageSerializer

class ProductList(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user'.
    Create a follower, i.e. follow a user if logged in.
    Perform_create: associate the current logged in user with a follower.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductImages(generics.ListCreateAPIView):
    """
    List all followers, i.e. all instances of a user
    following another user'.
    Create a follower, i.e. follow a user if logged in.
    Perform_create: associate the current logged in user with a follower.
    """
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = ProductImage.objects.all()

    # def perform_create(self, serializer):
    #     print(self.request.image)
    #     # serializer.save(product=self.request.product)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer # renders nice looking form in the UI
    permission_classes = [IsOwnerOrReadOnly] #only post owner can edit or delete post
    queryset = Product.objects.all()
