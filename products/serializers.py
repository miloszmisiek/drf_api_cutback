from rest_framework import serializers
from ratings.serializers import RatingSerializer
from .models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = ProductImage
        fields = ('id', 'product','product_name', 'image' )
        
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.ChoiceField(choices=Product.CATEGORIES)
    category_name = serializers.ReadOnlyField(source='get_category_display')
    price_currency = serializers.ChoiceField(choices=Product.CURRENCY_CHOICES)
    gallery = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    # ratings_count = serializers.ReadOnlyField()
    # score_count_1 = serializers.ReadOnlyField()
    # score_count_2 = serializers.ReadOnlyField()
    # score_count_3 = serializers.ReadOnlyField()
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
        scores = []
        for dict in rating_data:
            for k,v in dict.items():
                scores.append(v) if k == "score" else None
        return_dict = {item: scores.count(item) for item in scores}
        return_dict["all_scores"] = Product.objects.get(pk=product.id).all_scores
        return_dict["avg"] = Product.objects.get(pk=product.id).avg_score
        return return_dict
    
    # def get_category(self, category):
    #     return category.get_category_display()

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'category', 'category_name',
            'price','price_currency', 'title', 'description', 'brand',
            'inStock', 'created_at', 'updated_at', 'gallery', 'scores',
            # 'ratings_count', 'score_count_1',
            # 'score_count_2', 'score_count_3', 'score_count_4', 'score_count_5', 'score_avg',

        )
        