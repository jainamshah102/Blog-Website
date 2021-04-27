from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
import blog
import uuid
import os

MALE_IMG_URL = 'https://firebasestorage.googleapis.com/v0/b/blog-website-f447d.appspot.com/o/avatars%2Fmale.jpg?alt=media&token=54166618-78b2-4d46-b214-0ac5538ab7d4'
FEMALE_IMG_URL = 'https://firebasestorage.googleapis.com/v0/b/blog-website-f447d.appspot.com/o/avatars%2Ffemale.jpg?alt=media&token=0382139f-63e4-4b59-9f4d-eb9aac04e879'


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
    avatar = models.TextField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):

        if self.gender and (self.avatar in (MALE_IMG_URL, FEMALE_IMG_URL) or not self.avatar):
            self.avatar = MALE_IMG_URL if self.gender == "M" else FEMALE_IMG_URL

        super().save(*args, **kwargs)

    def edit_save(self, *args, **kwargs):
        super().save(*args, **kwargs)



    def followers(self):
        return Follow.objects.filter(author=self).count()

    def publishes(self):
        return blog.models.Blog.objects.filter(author=self, status=1).count()


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} {self.author.email}"
