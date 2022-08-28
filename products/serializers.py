from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField
from ratings.serializers import RatingSerializer
from .models import Product, ProductImage, Location
from ratings.models import Rating


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model. Product title added for clarity.
    """
    product_name = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'product_name', 'image')


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model.
    """
    class Meta:
        model = Location
        fields = ('id', 'address', 'city', 'country')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Handles nested serializers for ImageSerializer,
    RatingSerializer and LocationSerilizer.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    category = serializers.ChoiceField(choices=Product.CATEGORIES)
    category_name = serializers.ReadOnlyField(source='get_category_display')
    price = MoneyField(max_digits=10, decimal_places=2, required=True)
    price_currency = serializers.ChoiceField(choices=Product.CURRENCY_CHOICES)
    gallery = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Method checks if the current user is the owner of the profile
        and returns boolean value.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_gallery(self, product):
        """
        Loops through ImageSerializer data and returns list of images as URLs.
        """
        return_list = []
        gallery_data = ImageSerializer(
            product.product_images.all(),
            many=True).data
        for dict in gallery_data:
            for k, v in dict.items():
                return_list.append(v) if k == "image" else None
        return return_list

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
        statistics = {
            f'score_count_{n}': 0
            for n in range(1, len(Rating.RATE_CHOICES)+1)
        }
        statistics["all_scores"] = Product.objects.get(
            pk=product.id).all_scores if not None else None
        statistics["avg"] = Product.objects.get(
            pk=product.id).avg_score
        for dict in rating_data:
            for k, v in dict.items():
                if k == 'score':
                    statistics[f'score_count_{v}'] += 1
        return_data = {
            'data': rating_data,
            'statistics': statistics,
        }

        return return_data if rating_data else {}

    def get_location(self, product):
        """
        Returns LocationSerializer data.
        """
        return LocationSerializer(
            product.product_location.all(),
            many=True).data

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'is_owner', 'category', 'category_name',
            'price', 'price_currency', 'title', 'description', 'brand',
            'inStock', 'created_at', 'updated_at', 'gallery', 'scores',
            'location',
        )
