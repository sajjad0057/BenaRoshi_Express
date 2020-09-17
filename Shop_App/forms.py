from django import forms
from Shop_App.models import Category,Product

# Create Forms

        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('category',)
