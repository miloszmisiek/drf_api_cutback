from django.db.models import fields
from rest_framework import serializers

from .models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source='product.title')
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image' )
        #print(model)
        
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.ChoiceField(choices=Product.CATEGORIES)
    price_currency = serializers.ChoiceField(choices=Product.CURRENCY_CHOICES)
    gallery = serializers.SerializerMethodField()
    
    def get_gallery(self, product):
        return_list = []
        gallery_data = ImageSerializer(product.product_images.all(), many=True).data
        for dict in gallery_data:
            for k,v in dict.items():
                return_list.append(v) if k == "image" else None
        return return_list
    
    # def get_category(self, category):
    #     return category.get_category_display()

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'category', 
            'price','price_currency', 'title', 'description', 'brand',
            'inStock', 'created_at', 'updated_at', 'gallery'
        )
        