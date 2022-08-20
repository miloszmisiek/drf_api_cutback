from django.urls import path
from products import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/images/', views.ProductImages.as_view(),)
    # path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]