from django.db import models
from user.models import User
from django.utils.text import slugify


STATUS = (
    (0, 'Draft'),
    (1, 'Publish'),
)


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField()
    slug = models.SlugField(max_length=200)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
