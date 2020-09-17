from django.db import models
# To create a custom User model and Admin Panel...
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy

# To automatically create OneToOne objects
from django.db.models.signals import post_save
from django.dispatch import receiver




# Create your models here.

class MyUserManager(BaseUserManager):
    ''' A custom MyUserManager to deal with emails as unique identifier '''
    def _create_user(self,email,password,**extra_fields):
        ''' Create and saves a user with a given email and password '''
        
        
        if not email:
            raise ValueError('The Email Must Be Set..')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser = True')
        
        return self._create_user(email,password,**extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True,null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default= False,
        help_text=ugettext_lazy('Designates wheather the user can log in this site')
        
    )
    
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy('Designates wheather this user should be treated as active.Unselect this instead of deleting accounts')
    )
    
    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    username = models.CharField(max_length=264,blank=True)
    full_name = models.CharField(max_length=264,blank=True)
    address_1 = models.TextField(max_length=300,blank=True)
    city = models.CharField(max_length=40,blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=50,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}\'s profiles'
    
    
    '''By this function(it's userdefine function) Cheaking fileds are  set blank or not blank'''
    def is_fully_field(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        
        for field in fields_names:
            value = getattr(self,field)
            if value is None or value=='':
                return False
        return True
    
    
# for receving signal and execute action :

@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)  #By this automatically create a Profile object by user instance.
    
@receiver(post_save,sender = User)
def save_profile(sender,instance,**kwargs):  # By this function ,execute change in Profile models for any change in User model 
    instance.profile.save()


            
            
                
        
    
    
        