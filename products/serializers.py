from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from ratings.serializers import RatingSerializer
from .models import Product, ProductImage
from ratings.models import Rating
from profiles.serializers import ProfileSerializer


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model. Product title added for clarity.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    product_name = serializers.ReadOnlyField(source='product.title')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Method checks if the current user is the owner of the Image
        and returns boolean value.
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = ProductImage
        fields = ('id', 'owner', 'is_owner',
                  'product', 'product_name', 'image')


class ProductSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for Product model.
    Handles nested serializers for ImageSerializer,
    RatingSerializer.
    """
    owner_profile = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.ReadOnlyField(source='get_category_display')
    gallery = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    country = CountryField(country_dict=True)


    def get_is_owner(self, obj):
        """
        Method checks if the current user is the owner of the profile
        and returns boolean value.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_owner_profile(self, product):
        """
        Loops through ImageSerializer data and returns list of images as URLs.
        """
        request = self.context['request']
        return ProfileSerializer(
            product.owner.profile, context={'request': request}).data

    def get_gallery(self, product):
        """
        Loops through ImageSerializer data and returns list of images as URLs.
        """
        request = self.context['request']
        return ImageSerializer(
            product.product_images.all(),
            many=True, context={'request': request}).data

    def get_scores(self, product):
        """
        Loops through RatingSerializer data and
        returns data object with RatingSerializer data
        and statistics object containing counters for data.
        Returns empty object for empty data.
        """
        request = self.context['request']
        rating_data = RatingSerializer(
            product.product_rating.all(),
            many=True,
            context={'request': request}).data
        scores = {f'star_{n}': 0
                  for n in range(1, len(Rating.RATE_CHOICES)+1)}
        statistics = {}
        statistics["scores"] = scores
        statistics["all_scores"] = Product.objects.get(
            pk=product.id).all_scores
        statistics["avg"] = Product.objects.get(
            pk=product.id).avg_score
        for dict in rating_data:
            for k, v in dict.items():
                if k == 'score':
                    scores[f'star_{v}'] += 1
        return_data = {
            'data': rating_data if rating_data else [],
            'statistics': statistics,
        }

        return return_data

    class Meta:
        model = Product
        fields = (
            'id', 'owner_profile', 'category', 'category_name',
            'price', 'price_currency', 'title', 'description', 'brand',
            'in_stock', 'street', 'city', 'country', 'created_at', 'updated_at', 
            'gallery', 'scores', 'comments_count',
        )
