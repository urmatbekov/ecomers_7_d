from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


# Create your models here.
def content_file_name(instance, filename):
    return '/'.join(['avatars', instance.username, filename])


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False)
    avatar = ThumbnailerImageField(upload_to=content_file_name, blank=True, null=True)
    country = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)

    def get_avatar(self):
        if self.avatar:
            return self.avatar['avatar'].url
        return None

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'


class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    customer_phone = models.CharField(max_length=30)
    customer_address = models.CharField(max_length=50)
    SEX_CHOICES = [("M", 'Male'), ('F', 'Female')]
    customer_gender = models.CharField(choices=SEX_CHOICES, max_length=1)
