from django.urls import path
from .views import category_list, category_create, category_update, category_delete, product_list, product_create, product_update, product_delete

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<int:pk>/update/', category_update, name='category_update'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),
    path('products/', product_list, name='product_list'),
    path('products/category/<int:category_id>/', product_list, name='product_list_by_category'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
]
