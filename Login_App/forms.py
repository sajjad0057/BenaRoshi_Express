from django import forms
from django.forms import ModelForm
from Login_App.models import User,Profile
from django.contrib.auth.forms import UserCreationForm

#forms

# We import directly ModelForm so We can Use ModelForm instead of forms.ModelForm ...
class ProfileForm(ModelForm):
    class Meta():
        model = Profile
        exclude = ('user',)
        
        

class SignUpForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('email','password1','password2',)
        
        
 
