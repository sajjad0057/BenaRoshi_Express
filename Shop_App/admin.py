from django.contrib import admin
from Shop_App.models import Category,Product

# Register your models here.

admin.site.site_header = 'BenarosHi | Administration'
admin.site.site_title = 'BenarosHi'
admin.site.index_title = 'Welcome To BenarosHi Admin Site'



admin.site.register(Category)
admin.site.register(Product)