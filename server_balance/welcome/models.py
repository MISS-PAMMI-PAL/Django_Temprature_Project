from django.db import models
from django.contrib.auth.models import User
from myconst.models import MyState

import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img

from django.db.models.signals import post_delete
from django.dispatch import receiver


class UserProfile(models.Model):
    SO_WO = (
        (0, 'Son of'),
        (1, 'Wife of'),
        (2, 'Care of'),
        (3, 'DaughterOf'),
    )
    GENDER = (
        (0, 'Male'),
        (1, 'Female'),
    )  
    NOMINEE_RELATION = (
        (0, 'Father'),
        (1, 'Mother'),
        (2, 'Brother'),
        (3, 'Sister'),
        (4, 'Husband'),
        (5, 'Wife'),
        (6, 'Son'),
        (7, 'Daughter'),
    )

    def profile_name(instance, filename):
        name, ext = filename.split('.')
        first_path = f"{instance.user_ins.username}"
        file_path = f"profile_img/Img_{first_path}.{ext}"
        return file_path

    user_ins = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    profile_img = models.ImageField(upload_to=profile_name, max_length=30, null=True, blank=True) # getattr(): attribute name must be string
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.BooleanField(choices=GENDER, default=0, null=True, blank=True) 
    so_wo = models.PositiveSmallIntegerField(choices=SO_WO, default=0, null=True, blank=True) 
    so_name = models.CharField(max_length=30, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)
    building = models.CharField(max_length=30, null=True, blank=True)
    colony = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    post = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=30, null=True, blank=True)
    police_station = models.CharField(max_length=30, null=True, blank=True)
    dist = models.CharField(max_length=30, null=True, blank=True)
    state = models.ForeignKey(MyState, on_delete=models.CASCADE, related_name='profile_mystate', null=True, blank=True) 
    nominee_name = models.CharField(max_length=30, null=True, blank=True)
    nominee_rel = models.PositiveSmallIntegerField(choices=NOMINEE_RELATION, default=7, null=True, blank=True)

    def save(self, *args, **kwargs):
        width = 300
        height = 300
        size = (width, height)
        isSame = False
        if self.profile_img:
            try:
                this = UserProfile.objects.get(id=self.id)
                if this.profile_img == self.profile_img:
                    isSame = True
            except:
                pass  # when new photo then we do nothing, normal case

            new_image = Img.open(self.profile_img)

            # if dont use resize
            (imw, imh) = new_image.size
            if (imw > width) or (imh > height):
                new_image.thumbnail(size, Img.ANTIALIAS)

            # If RGBA, convert transparency
            if new_image.mode == "RGBA":
                new_image.load()
                background = Img.new("RGB", new_image.size, (255, 255, 255))
                background.paste(new_image, mask=new_image.split()[3])  # 3 is the alpha channel
                new_image = background

            output = BytesIO()
            #image_resize = image.resize((300, 300))
            new_image.save(output, format='JPEG', quality=10)
            output.seek(0)
            self.profile_img = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.profile_img.name.split('.')[0],
                                                    'image/jpeg', sys.getsizeof(output), None)

        try:
            this = UserProfile.objects.get(id=self.id)
            if this.profile_img == self.profile_img or isSame:
                self.profile_img = this.profile_img
            else:
                this.profile_img.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case

        super(UserProfile, self).save(*args, **kwargs)

        '''
        @receiver(post_delete, sender=Mymodel)
        def photo_post_delete_handler(sender, **kwargs):
            instance = kwargs['instance']
            storage, path = instance.photo.storage, instance.photo.path
            if (path!='.') and (path!='/') and (path!='photo/') and (path!='photo/.'):
                storage.delete(path)
                
                
           https://stackoverflow.com/questions/24387022/django-save-override-imagefield-handling/24396201#24396201     
        '''

class ContactTo(models.Model):  # only-handle-by-master, footer information collect krna
    name = models.CharField(max_length=30, null=True, blank=True)    # if is_heading=True then only title show
    mobile = models.CharField(max_length=15, null=True, blank=True)   # quarry
    email = models.CharField(max_length=30, null=True, blank=True)    # answer
    query = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Traffic(models.Model):
    visit = models.PositiveIntegerField(null=True, blank=True, default=0)
    login = models.PositiveIntegerField(null=True, blank=True, default=0)
    login_failed = models.PositiveIntegerField(null=True, blank=True, default=0)
    reset_pwd = models.PositiveIntegerField(null=True, blank=True, default=0) 
    guest = models.PositiveIntegerField(null=True, blank=True, default=0) # new_guest registration
    device_active = models.PositiveIntegerField(null=True, blank=True, default=0)  
    msg = models.PositiveIntegerField(null=True, blank=True, default=0)
    traffic_date = models.DateField(auto_created=True)

class UserDesc(models.Model):
    user_ins = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdesc_user')
    device_ip = models.CharField(max_length=50, null=True, blank=True)
    device_loc = models.CharField(max_length=50, null=True, blank=True)           #===========
    sms_life = models.PositiveSmallIntegerField(null=True, blank=True, default=0)       # allow otp 5 times
    last_login = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # modal_pop = models.BooleanField(True, null=True, blank=True)  #========

    def __str__(self):
        return str(self.user_ins)
