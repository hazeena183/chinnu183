from django.contrib import admin

# Register your models here.
from .models import Item,Tutorial

admin.site.register(Item)
admin.site.register(Tutorial)
