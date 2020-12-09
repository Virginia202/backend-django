from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Create and return a `User` with super powers."""
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=100, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField( default=False)
    photo = CloudinaryField('photo', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):

        return self.email

    @property
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def token(self):
        """
        This method allows us to get the jwt token by calling the user.token
        method.
        """
        return self.generate_jwt_token()

    def generate_jwt_token(self):

        user_details = {'email': self.email,
                        'username': self.username}
        token = jwt.encode(
            {
                'user_data': user_details,
                'exp': datetime.now() + timedelta(hours=72)
            }, settings.SECRET_KEY, algorithm='HS256'
            )
        return token.decode('utf-8')


class Profile (models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    status = models.BooleanField()
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True)
    profile_pic = CloudinaryField('Profile pic', default = 'profile.jpg')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    def save_profile(self):
        self.save
    def delete_profile(self):
        self.delete()
        
class Post(models.Model):
    item = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    contact = models.CharField(max_length=100)
    image = CloudinaryField('image')
    date_posted = models.DateTimeField(_('date posted'), auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} post'

    def save_post(self):
        self.save
    def delete_post(self):
        self.delete()    