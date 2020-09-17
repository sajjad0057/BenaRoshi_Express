from django.urls import path
from Shop_App import views


app_name = 'Shop_App'

urlpatterns = [
    path('',views.home.as_view(),name='home'),
    path('product/<pk>/',views.ProductDetail.as_view(),name ='product_detail'),
    path('category/',views.category.as_view(),name='category'),
    path('add_category/',views.add_category.as_view(),name='add_category'),
    path('add_product/<pk>/',views.AddProduct,name='add_product'),
    
    
]
 