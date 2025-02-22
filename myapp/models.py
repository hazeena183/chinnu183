from django.db import models

# Create your models here.

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    attached_file = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.title

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=False,default="hhh")
    full_name = models.CharField(max_length=100,default="dddd")


from django.db import models

class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)

from django.db import models

class Item(models.Model):
	category = models.CharField(max_length=255)
	subcategory = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	amount = models.PositiveIntegerField()

	def __str__(self) -> str:
		return self.name
