from django.urls import path, include
from rest_framework import routers
from .views import (StoreListAPIView, StoreDetailAPIView, ContactView,
                    AddressView, StoreMenuListAPIView, StoreMenuDetailAPIView,
                    ProductListAPIView, ProductDetailAPIView,
                    OrderView, CourierView, ReviewCreateAPIView, CategoryListAPIView, CategoryDetailAPIView,
                    UserProfileListAPIView, UserProfileDetailAPIView, ReviewListAPIView,
                    ReviewUpdateAPIView, RegisterView, CustomLoginView, LogoutView)

router = routers.SimpleRouter()

router.register(r'contact', ContactView, basename='contact_list')
router.register(r'address', AddressView, basename='address_list')
router.register(r'order', OrderView, basename='order_list')
router.register(r'courier', CourierView, basename='courier_list')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('auth/user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('menu/', StoreMenuListAPIView.as_view(), name='store_menu_list'),
    path('menu/<int:pk>/', StoreMenuDetailAPIView.as_view(), name='store_menu_detail'),
    path('product', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('reviews/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('reviews/', ReviewListAPIView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewUpdateAPIView.as_view(), name='review_update'),
]
