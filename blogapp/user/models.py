from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
import uuid
import os


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


def rename_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars/', filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    about = models.CharField(max_length=1000, blank=True, default="")
    name = models.CharField(max_length=100, blank=True, default="")
    gender = models.CharField('gender', max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to=rename_file_upload, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        
        if self.gender and (self.avatar in ("male.jpg", "female.jpg") or not self.avatar):
            self.avatar = 'male.jpg' if self.gender == "M" else 'female.jpg'

        super().save(*args, **kwargs)


    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.author.email}"
