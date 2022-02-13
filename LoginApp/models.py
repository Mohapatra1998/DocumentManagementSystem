from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode, os
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils.translation import gettext_lazy as _


# Create your models here.
class MyUser(AbstractUser):
    user_type_choice = ((1, "Admin"), (2, "Manager"), (3, "User"))
    user_type = models.CharField(default=1, choices=user_type_choice, max_length=20)

   


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class User(models.Model):
    id = models.AutoField(primary_key=True)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



class Document(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    aprove_type_data = ((1, "Aproved"), (2, "Rejected"), (3, "Pending"))
    aproved_by_manager = models.CharField(default=3, choices=aprove_type_data, max_length=10)
    aproved_by_admin = models.CharField(default=3, choices=aprove_type_data, max_length=10)
    name = models.CharField(max_length=225)
    file = models.FileField(upload_to='document')
    qr_code = models.CharField(max_length=200, blank=True, null=True )
    description = models.TextField()
    FILE_CHOICES = (
        ('DOC', 'DOC'),
        ('PDF', 'PDF'),
        ('EXE', 'EXE'),
    )
    file_type = models.CharField(choices=FILE_CHOICES, max_length=30, default='')
    file_numble = models.IntegerField(default=0)
    review = models.IntegerField(default=0)
    department_choice = (
        ('Civil', 'Civil'),
        ('Mechanical', 'Mechanical'),
        ('BCA', 'BCA'),
        ('Computer', 'Computer'),
    )
    department = models.CharField(max_length=30, blank=True, null=True, choices=department_choice, default='')
    reject_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"
    # def save(self, *args, **kwargs) :
    #     link = "http://127.0.0.1:8000/media/document/" + self.file
    #     qr = self.qr_generate(link)
    #     self.qr.save(link + '.png', BytesIO(qr), save=False)   


# signal
@receiver(post_save, sender=MyUser)
def create_user_data(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(myuser=instance)
        if instance.user_type == 2:
            Manager.objects.create(myuser=instance)
        if instance.user_type == 3:
            User.objects.create(myuser=instance)


@receiver(post_save, sender=MyUser)
def save_user_data(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.manager.save()
    if instance.user_type == 3:
        instance.user.save()
