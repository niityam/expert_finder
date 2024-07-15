import django_filters
from .models import *

class expertiseFilter(django_filters.FilterSet):
    class Meta:
        model = expertise
        fields = '__all__'
