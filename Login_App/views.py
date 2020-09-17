from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
#Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
#forms and models
from Login_App.forms import ProfileForm,SignUpForm
from Login_App.models import User, Profile
# For show messages need import messages module
from django.contrib import messages



# Create your views here.

def sign_up(request):
    form = SignUpForm()
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully !")
            return HttpResponseRedirect(reverse('Login_App:login'))
    return render(request,'Login_App/sign_up.html',context={'form':form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('Shop_App:home'))
            
    return render(request,'Login_App/login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    messages.info(request,'You Are Logged Out .')
    return HttpResponseRedirect(reverse('Shop_App:home'))


@login_required
def user_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Changed Saved Successfully !")
            form = ProfileForm(instance=user_profile)
    return render(request,'Login_App/change_profile.html',context={'form':form})
    
        
    
