from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Order_App.models import Cart,Order
from Shop_App.models import Product

# Create your views here.

@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    #print('item---->',item)
    order_item = Cart.objects.get_or_create(item=item, user=request.user,purchased=False)
    #print('Order_item----->',order_item)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    #print('order_qs-------->',order_qs)
    
    if order_qs.exists():
        #print('if order_qs exists()--->',order_qs[0])
        order = order_qs[0]
        #print('--------->',order)
        if order.orderitems.filter(item=item).exists():
            #print(order_item)
            #print(order_item[0])
            #print(order_item[0].quantity)
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request,'This item quantity has updated.')
            return redirect('Shop_App:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request,'This item has added to your cart.')
            return redirect('Shop_App:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,'This item has added to your cart.')
        return redirect('Shop_App:home')



@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    #print(carts)
    #print(carts[0])
    orders = Order.objects.filter(user=request.user,ordered=False)
    #print(orders)
    if carts and orders:
        order = orders[0]
        
        #print(order)
        return render(request,"Order_App/cart.html",context={'carts':carts,'order':order})
    else:
        messages.warning(request,"Yout don,t have an any item in your cart .")
        return redirect('Shop_App:home')
    
    

@login_required
def remove_from_cart(request,pk):    # here "if order_qs:" and "if order_qs.exists():" are work same. But recommanded to using .exists()!
    item = get_object_or_404(Product,pk=pk)
    order_qs = Order.objects.filter(user = request.user,ordered=False)
    if order_qs:     
        #print(order_qs)    
        order = order_qs[0]
        #print(order)
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item,user = request.user,purchased=False)[0]
            #print(order_item)
            #print(order_item.pk)
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.info(request,"This item has been removed from cart !")
            return redirect('Order_App:cart')
        else:
            messages.info(request,"This item haven't in your cart !")
            return redirect("Shop_App:home")
            
        
        
    else:
        messages.info(request,"You Don't have an active Order in Cart !")
        return redirect("Shop_App:home")
    
    


@login_required
def increase_cart(request,pk):   
    item = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists(): # here "if order_qs:" and "if order_qs.exists():" are work same. But recommanded to using .exists()!
        order = order_qs[0]
        if order.orderitems.filter(item=item):
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            print(order_item)
            if order_item.quantity >=1:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,f' {item.name} quantiy has been updated ! ')
                return redirect('Order_App:cart')
            
        else:
            messages.info(request,f'{item.name} is not in your cart !')
            return redirect('Shop_App:home')

            
    else:
        messages.info(request,"You don't have an active order !")
        return redirect("Shop_App:home")
    
    
@login_required
def decrease_cart(request,pk):   
    item = Product.objects.get(pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists(): # here "if order_qs:" and "if order_qs.exists():" are work same. But recommanded to using .exists()!
        order = order_qs[0]
        if order.orderitems.filter(item=item):
            order_item = Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            print(order_item)
            if order_item.quantity >1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request,f' {item.name} quantiy has been updated ! ')
                return redirect('Order_App:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request,f' {item.name} has been removed from your cart ! ')
                return redirect('Order_App:cart')
                
        else:
            messages.info(request,f'{item.name} is not in your cart !')
            return redirect('Shop_App:home')
            

            
    else:
        messages.info(request,"You don't have an active order !")
        return redirect("Shop_App:home")