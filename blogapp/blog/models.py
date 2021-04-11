from django.db import models
from user.models import User
from django.utils.text import slugify
from django.utils import timezone
from tinymce.models import HTMLField



def rename_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('blog/', filename)


STATUS = (
    (0, 'Draft'),
    (1, 'Publish'),
)


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = HTMLField()
    slug = models.SlugField(max_length=200)
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    published_on  = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def publish(self):
        self.published_on = timezone.now()
        self.status = 1
        super().save()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.blog.title}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    comment = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return f"{self.user.email} - {self.blog.title}"
