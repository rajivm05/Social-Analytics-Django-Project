from django.contrib import admin

# Register your models here.

from .models import SearchModel
admin.site.register(SearchModel)