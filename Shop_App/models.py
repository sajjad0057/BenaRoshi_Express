from django.db import models

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        verbose_name_plural = "Categories"
        

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category')
    product_image = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=264)
    preview_text = models.CharField(max_length=200,verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000,verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(blank=True,null=True,default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created',]
    

