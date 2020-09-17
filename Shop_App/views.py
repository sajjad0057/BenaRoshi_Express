from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView,DetailView,CreateView
from Shop_App.models import Category,Product
from Shop_App.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.


class home(ListView):
    model = Product
    template_name = 'Shop_App/home.html'

    
class ProductDetail(DetailView):
    model = Product
    template_name = 'Shop_App/product_details.html'
    
    
class category(ListView):
    model = Category
    template_name = 'Shop_App/category.html'
    

class add_category(LoginRequiredMixin,CreateView):
    model = Category
    fields = ('title',)
    template_name = 'Shop_App/category.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['flag']=True
        return context
    
    def form_valid(self,form):
        form.save()
        messages.info(self.request,"A new Category Add Successfull !")
        return HttpResponseRedirect(reverse("Shop_App:category"))


    
@login_required
def AddProduct(request,pk):
    flag=False
    category = Category.objects.get(pk=pk)
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.category = category
            form.save()
            flag = True
            messages.info(request,"Product Added Successfully !")
            return HttpResponseRedirect(reverse('Shop_App:add_product',kwargs={'pk':pk}))
    return render(request,'Shop_App/add_product.html',context={'form':form,'flag':flag})
        
            
           



    