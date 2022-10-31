from ast import mod
from django.db import models


#To create a custom user model and admin panel
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy

#To create automatically create one to one objects
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyUserManager(BaseUserManager):

    """A custom manager to deal with emails and custom identifiers"""

    def _create_user(self,email,password, **extra_fields):
        """Create and saves a user with a given email and password"""

        if not email:
            raise ValueError('The email must be set!')
        
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("usperuser must have is_staff=True")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser=True')
        
        return self._create_user(email,password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email=models.EmailField(unique=True,null=False)
    is_staff=models.BooleanField(
        gettext_lazy('staff_status'),default=False,
        help_text=gettext_lazy('designets wheter the user can loin to this site'),
    )

    is_active=models.BooleanField(
        gettext_lazy('active'),default=True,
        help_text=gettext_lazy('designets wheter the user can loin to this site'),
    )

    USERNAME_FIELD='email'

    objects=MyUserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

gender_info=(('Male','Male'),('Female','Female'),('Other','Other'))
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    fullName=models.CharField(max_length=264,blank=True)
    user_phone=models.CharField(max_length=15,blank=True)
    gender=models.CharField(max_length=10,choices=gender_info,default='Male')
    user_photo=models.ImageField( upload_to='admin', height_field=None, width_field=None, max_length=None)
    dateOfJoin=models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)
    user_catagory=models.CharField(max_length=10,default='PATIENT')                                      

    def __str__(self):
        return self.fullName+"'s profile"

    def fully_filled(self):
        fields_name=[f.name for f in self._meta.get_fields()]

        for field_name in fields_name:
            value=getattr(self,field_name)

            if value is None or value=='':
                return False

        return True

@receiver(post_save,sender=User)

def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()


    