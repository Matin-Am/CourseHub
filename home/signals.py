from django.db.models.signals import post_save,post_delete,m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from .models import Course


@receiver(signal=[post_save,post_delete],sender=Course)
def delete_cache_on_course_change(sender,**kwargs):
    cache.delete_pattern(f"*courses_list*")


@receiver(signal=m2m_changed,sender=Course)
def delete_cache_on_m2m_change(sender,**kwargs):
    if kwargs["action"] in ["post_add","post_remove","post_clear"]:
        for user_id in kwargs["pk_set"]:
            cache.delete_pattern(f"*courses_list_{user_id}")

