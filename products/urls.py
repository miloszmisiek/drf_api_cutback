from django.urls import path
from products import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/images/', views.ProductImages.as_view(),),
    path('products/images/<int:pk>/', views.ProductImagesDetail.as_view(),),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('products/choices/', views.ProductChoicesView.as_view()),
]
