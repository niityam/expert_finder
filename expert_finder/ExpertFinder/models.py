from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
import random

class expertise(models.Model):
    imgno = models.IntegerField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField(help_text='Estimated price, if it varies keep 0 ')
    time_to_complete = models.CharField(max_length=10, help_text='Estimate time to complete that')
    location = models.CharField(max_length=100, help_text='Area, City')
    date_posted = models.DateTimeField(default=timezone.now)
    expert_identity = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, help_text='Add synonyms of expertise, so client find you easily')
    description = models.TextField(help_text='Tell about your Expertise in detail ')

    def get_absolute_url(self):
        return reverse('expertise-detail',kwargs={'pk' : self.pk})

    def __str__(self):
        template = '{0.title}, {0.expert_identity}'
        return template.format(self)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    city = models.CharField(default='Ahmedabad', max_length= 30, help_text="Enter city you live in")
    address = models.TextField(default='NONE', help_text="Enter Address or Google Maps Links(open maps -> hold on your home -> share (copylink) -> paste here")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

#AN
class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Completed', 'Completed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(expertise, on_delete = models.CASCADE)
    address = models.TextField(default='No address avalible')
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')
    delivery_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Item'

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'pk' : self.pk
        })

    def update_status_url(self):
        return reverse("update_status", kwargs={
            'pk' : self.pk
        })