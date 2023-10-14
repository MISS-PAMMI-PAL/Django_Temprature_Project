from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save


from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class MyState(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

class UserNotifications(models.Model):
    news = models.TextField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=False)


#========================== slide =============================================
def increment_fun(class_name):
    try:
        temp_id = class_name.objects.order_by('-id')
        if temp_id.exists():
            return int(temp_id.first().id) + 1
        else:
            return 1
    except:
        return 1

class SlideContent(models.Model):   # slide link content only 0-4 page  or doc for download and show in banner link
    def slide_content_name(instance, filename):
        name, ext = filename.split('.')
        if instance.id == None:
            file_path = f"slide_content/docs_{increment_fun(SlideContent)}.{ext}"
        else:
            file_path = f"slide_content/docs_{instance.id}.{ext}"
        return file_path

    title = models.CharField(max_length=30, null=True, blank=True)
    slide_docs = models.FileField(upload_to=slide_content_name, null=True, blank=True)
    desc_h = models.TextField(max_length=2000, null=True, blank=True)
    desc_e = models.TextField(max_length=2000, null=True, blank=True)
    is_show_text = models.BooleanField(default=True)
    is_download = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # work ====================================================================================


@receiver(pre_save, sender=SlideContent)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).slide_docs.path
        try:
            new_img = instance.slide_docs.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

#==================================================================