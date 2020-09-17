from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from Order_App.models import Order,Cart
from Payment_App.models import BillingAddress
from Payment_App.forms import BillingForm
from django.contrib.auth.decorators import login_required
# Messages
from django.contrib import messages
# for payments
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user = request.user)[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST,instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    #print(order_qs)
    order_items = order_qs[0].orderitems.all()
    #print(order_items)
    order_total = order_qs[0].get_totals()
    #print(order_total)
    
    
    return render(request,'Payment_App/checkout.html',context={'form':form,'order_items':order_items,
                                                               'order_total':order_total,'saved_address':saved_address})



@login_required
def payment(request):
    saved_address = BillingAddress.objects.get(user=request.user)
    '''Here if we use get() query_set,we don't have need to use indexing for access object value,
    otherwise we need  indexing  to access saved_address value  '''
    #print(saved_address)
    if not saved_address.is_fully_filled():
        messages.warning(request,"Please Complete Your Shipping Address !")
        return redirect('Payment_App:checkout')
    if not request.user.profile.is_fully_field():
        messages.warning(request,"Please Complete Your Profile Info !")
        return redirect('Login_App:profile')
    
    # From SSlCOMMERZ gmail notification:
    store_id = 'sajja5f61279af322c'
    API_key ='sajja5f61279af322c@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)
    #print('request---->',request)
    status_url = request.build_absolute_uri(reverse('Payment_App:complete'))
    #print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                        cancel_url=status_url, ipn_url=status_url)
    
    order_qs = Order.objects.get(user=request.user,ordered=False)
    '''Here if we use get() query_set,we don't have need to use indexing for access object value,
    otherwise we need  indexing  to access objects value  '''
    #print(order_qs)
    order_items = order_qs.orderitems.all()
    order_items_count = order_qs.orderitems.count()
    order_total = order_qs.get_totals()
    
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',product_name=order_items,
                                      num_of_item=order_items_count, shipping_method='Courier', product_profile='None')
    
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1,
                                city=current_user.profile.city,postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    response_data = mypayment.init_payment()
    #print(response_data)
    
    
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        #print(payment_data)
        status = payment_data['status']

        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request,' your payment has been completed successfully !')
            return HttpResponseRedirect(reverse('Payment_App:purchase',kwargs={
                'val_id':val_id,'tran_id':tran_id
            }))
        elif status == 'FAILED':
            messages.warning(request,' Oops ! Your payment had been failed ! Please try again. this page is redirect autometically, please wait 5 sec.')
        
    return render(request,'Payment_App/complete.html',context={})


@login_required
def purchase(request,val_id,tran_id):
    '''Here if we use get() query_set,we don't have need to use indexing for access object value,
    otherwise we need  indexing  to access objects value  '''
    order_q = Order.objects.filter(user=request.user,ordered=False)
    #print('order_q---->',order_q)
    #print('order_q[0]---->',order_q[0])
    order_qs = Order.objects.get(user=request.user,ordered=False)
    #print('order_qs---->',order_qs)
    order_qs.ordered=True
    order_qs.paymentId=val_id
    order_qs.orderId=tran_id
    order_qs.save()
    cart_item = Cart.objects.filter(user=request.user,purchased=False)
    #print('cart_item----->',cart_item)
    for item in cart_item:
        #print('item---->',item)
        item.purchased=True
        item.save()
    return HttpResponseRedirect(reverse('Shop_App:home'))
    

@login_required
def user_orders(request):
    try:
        orders = Order.objects.filter(user=request.user,ordered=True)
        dict = {'orders':orders}
    except:
        messages.warning(request,"Yon don't have any active order now ! ")
        return redirect('Shop_App:home')
    return render(request,'Payment_App/order.html',context=dict)


    
