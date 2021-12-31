from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

#Create your models here.
class UserProfileManager(BaseUserManager):
    """"Manager for UserProfile"""
    def create_user(self,email,name,password = None):
        """" Create a new a UserProfile"""
        if not email: #Checking for null value or empty string
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email = email,name = name)
        user.set_password(password) #To store the database as hash
        user.save(using = self._db) #Saving the object

        return user

    def create_superuser(self,email,name,password):
        """Create and save a superuser"""
        user = self.create_user(email , name, password) #Firstly creating the user using the function defined before
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """
    Database models for users in the system
    """
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email' #Makes the username for this class as email
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve the full name of user"""
        return self.name

    def get_short_name(self):
        """ Retrieve the short name of user"""
        return self.name

    def __str__(self):
        "Return string representation of the user"
        return self.email


class ProfileFeedItem(models.Model):
    """ Profile status update """
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,#Basically this is more of a best practice, in case we change the authentication model
                                # which at this moment in UserProfile.
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            """ Return the model as a string"""
            return self.status_text
