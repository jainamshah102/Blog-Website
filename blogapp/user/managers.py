from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

MALE_IMG_URL = 'https://firebasestorage.googleapis.com/v0/b/blog-website-f447d.appspot.com/o/avatars%2Fmale.jpg?alt=media&token=54166618-78b2-4d46-b214-0ac5538ab7d4'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', "Admin")
        extra_fields.setdefault('gender', "M")
        extra_fields.setdefault('avatar', MALE_IMG_URL)
        extra_fields.setdefault('about', 'White Ink Administrator')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
