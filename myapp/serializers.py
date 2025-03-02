from rest_framework import serializers
from .models import Tutorial


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')


from django.db.models import fields
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('category', 'subcategory', 'name', 'amount')

from rest_framework import serializers
from .models import Genre, Book

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)  # Display genre details instead of ID

    class Meta:
        model = Book
        fields = '__all__'
