from django.db import models

# Create your models here.


'''

'''




class Course(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
    



class Episode(models.Model):
    course = models.ForeignKey(Course , on_delete=models.CASCADE , related_name="episodes")
    video = models.FileField(upload_to='episodes/%Y/%M/%d/')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)


    def __str__(self):
        return f"{self.title} - {self.slug}"
