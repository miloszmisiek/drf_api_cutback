from rest_framework import serializers
from ratings.serializers import RatingSerializer
from .models import Product, ProductImage, Location
from ratings.models import Rating


class ImageSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = ProductImage
        fields = ('id', 'product','product_name', 'image' )

class LocationSerializer(serializers.ModelSerializer):
    # product_name = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = Location
        fields = ('id', 'address', 'city', 'country')
        
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.ChoiceField(choices=Product.CATEGORIES)
    category_name = serializers.ReadOnlyField(source='get_category_display')
    price_currency = serializers.ChoiceField(choices=Product.CURRENCY_CHOICES)
    gallery = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    # ratings_count = serializers.ReadOnlyField()
    # product_rating = serializers.ReadOnlyField()
    # score_count_2 = serializers.ReadOnlyField()
    # score_count_4 = serializers.ReadOnlyField()
    # score_count_5 = serializers.ReadOnlyField()
    # score_avg = serializers.ReadOnlyField()

    
    def get_gallery(self, product):
        return_list = []
        gallery_data = ImageSerializer(product.product_images.all(), many=True).data
        for dict in gallery_data:
            for k,v in dict.items():
                return_list.append(v) if k == "image" else None
        return return_list
    
    def get_scores(self, product):
        rating_data = RatingSerializer(product.product_rating.all(), many=True).data
        statistics = {f'score_count_{n}': 0 for n in range(1, len(Rating.RATE_CHOICES)+1)}
        statistics["all_scores"] = Product.objects.get(pk=product.id).all_scores if not None else None
        statistics["avg"] = Product.objects.get(pk=product.id).avg_score
        for dict in rating_data:
            for k,v in dict.items():
                if k == 'score':
                    statistics[f'score_count_{v}'] +=1
        return_data = {
            'data': rating_data,
            'statistics': statistics,
        }
        
        return return_data if rating_data else {}

    def get_location(self, product):
        return LocationSerializer(product.product_location.all(), many=True).data
    
    # def get_category(self, category):
    #     return category.get_category_display()

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'category', 'category_name',
            'price','price_currency', 'title', 'description', 'brand',
            'inStock', 'created_at', 'updated_at', 'gallery', 'scores',
            'location',
        )
        