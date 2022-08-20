from django.db.models import fields
from rest_framework import serializers

from .models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'image' )
        #print(model)
        
class ProductSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()
    
    def get_gallery(self, product):
        return_list = []
        gallery_data = ImageSerializer(product.product_images.all(), many=True).data
        for dict in gallery_data:
            for k,v in dict.items():
                return_list.append(v) if k == "image" else None
        return return_list

    class Meta:
        model = Product
        fields = (
            'id', 'owner', 'category', 
            'price', 'title', 'description', 'brand',
            'inStock', 'created_at', 'updated_at', 'gallery'
        )