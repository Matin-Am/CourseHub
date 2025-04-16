from django.contrib import admin
from .models import Episode , Course

# Register your models here.

admin.site.register(Episode)


class CourseAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)




admin.site.register(Course,CourseAdmin)

