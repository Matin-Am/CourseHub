from django.db import models
from django.urls import reverse
from django.conf import settings
from accounts.models import User
# Create your models here.


'''

'''




class Course(models.Model):
    user = models.ManyToManyField(User , related_name='courses')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    paid = models.BooleanField(default=True)
    price = models.PositiveIntegerField(null=True , blank=True)
    image = models.ImageField(upload_to='images/%Y/%M/%d/',blank=True , null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



class Episode(models.Model):
    course = models.ForeignKey(Course , on_delete=models.CASCADE , related_name="episodes")
    video = models.FileField(upload_to='episodes/%Y/%M/%d/')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)


    def __str__(self):
        return f"{self.title}"

    def get_absoulute_url(self):
        return reverse('home:video', args=[self.slug])