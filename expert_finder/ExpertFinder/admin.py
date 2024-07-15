from django.contrib import admin
from .models import expertise
from .models import Profile
from .models import CartItems

admin.site.register(expertise)
admin.site.register(Profile)
admin.site.register(CartItems)
