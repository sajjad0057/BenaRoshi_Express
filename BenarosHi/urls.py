from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Shop_App.urls')),
    path('account/',include('Login_App.urls')),
    path('shop/',include('Order_App.urls')),
    path('payment/',include('Payment_App.urls')),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
