from django.urls import path
from .api_views import (
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    ActiveProductListView, ProductSearchView,
    ProductByCategoryView, ProductImageUploadView,
    CategoryStatsView, ToggleProductActiveView,
    ProductFilterByPriceView, AveragePriceAPIView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('products/active/', ActiveProductListView.as_view(), name='active-products'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('products/by-category/<int:category_id>/', ProductByCategoryView.as_view(), name='products-by-category'),
    path('products/<int:pk>/upload-image/', ProductImageUploadView.as_view(), name='upload-product-image'),
    path('categories/stats/', CategoryStatsView.as_view(), name='category-stats'),
    path('products/<int:pk>/toggle-active/', ToggleProductActiveView.as_view(), name='toggle-product-active'),
    path('products/filter-by-price/', ProductFilterByPriceView.as_view(), name='filter-by-price'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('products/average-prices/', AveragePriceAPIView.as_view(), name='average-prices'),
]
