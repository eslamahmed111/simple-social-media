from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
# from accounts.models import User

# pip install misaka
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()

# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
#allow us to do a link from the post to group member  using the related_name="user_groups" to connect to the group members
register = template.Library()

class Group(models.Model):
    owner = models.ForeignKey(User,related_name='group_owner',on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="GroupMember")    #Through option Represents the intermediate table that you want to use.  This used when you want to associate extra data in the relationship

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)  #Calls the "real" save() method. 

    def get_absolute_url(self): #The generated url goes automatically to CreateVeiw
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    ''' This intermediate table used to add some extra methods and attributes to the manytomany relationship
        and also used to create a membership for joining and leaving groups'''
        
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user") 