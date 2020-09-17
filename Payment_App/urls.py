from django.urls import path
from Payment_App import views




app_name = 'Payment_App'

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('payment-here/',views.payment,name = 'payment'),
    path('payment-status/',views.complete,name='complete'),
    path('purchase/<val_id>/<tran_id>/',views.purchase,name='purchase'),
    path('orders/',views.user_orders,name='orders'),
    
]
