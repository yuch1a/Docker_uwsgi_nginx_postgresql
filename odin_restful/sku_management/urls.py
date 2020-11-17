from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product_delete'),
    path('skus/', views.SKUListView.as_view(), name='skus'),
    path('sku/create/', views.SKUCreate.as_view(), name='sku_create'),
    path('sku/<int:pk>/update/', views.SKUUpdate.as_view(), name='sku_update'),
    path('sku/<int:pk>/delete/', views.SKUDelete.as_view(), name='sku_delete'),
    path('sku/<int:pk>', views.SKUDetailView.as_view(), name='sku-detail'),
]