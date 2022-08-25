from django.contrib import admin
from .models import Product, ProductImage, Location


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class LocationAdmin(admin.StackedInline):
    model = Location
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, LocationAdmin]
 
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
