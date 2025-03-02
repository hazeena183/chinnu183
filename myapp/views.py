from django.shortcuts import render, get_object_or_404
from .forms import SimpleForm


from django.shortcuts import render
from .models import Task
from .forms import TaskForm
from rest_framework.decorators import api_view


def hello(request):
    return render(request, 'hello.html')
from django.shortcuts import render
from .forms import SimpleForm

def simple_form(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database)
            # Here, you can add your custom logic for handling the form submission.
            return render(request, 'form_success.html')
    else:
        form = SimpleForm()

    return render(request, 'simple_form.html', {'form': form})

from django.shortcuts import render, redirect


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list page
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        full_name = request.POST['full_name']

        # Add validation logic (e.g., check for existing username)

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('signup')

        UserProfile.objects.create(username=username, password=password, email=email, full_name=full_name)
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        return redirect('dashboard')

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Tutorial
from .serializers import TutorialSerializer, ItemSerializer
from rest_framework.decorators import api_view



@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()

        title = request.query_params.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)

        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, k):
    try:
        tutorial = Tutorial.objects.get(pk=k)
    except Tutorial.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)

    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item



class ItemAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            # If pk is provided, return details for a specific item
            item = get_object_or_404(Item, pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        else:
            # If no pk is provided, return a list of all items
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        item_serializer = ItemSerializer(data=request.data)

        if Item.objects.filter(**request.data).exists():
            return Response({'detail': 'This data already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, p):
        item = get_object_or_404(Item, pk=p)
        item_serializer = ItemSerializer(instance=item, data=request.data, partial=True)

        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data)
        else:
            return  Response(item_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import generics
from .models import Genre, Book
from .serializers import GenreSerializer, BookSerializer

# ✅ Genre Views
class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# ✅ Book Views
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# from django.contrib.auth.models import User
#
# user = User.objects.create_user('john', 'johndoe@example.com', 'john123')
#
# user.first_name = 'John'
# user.last_name = 'Doe'
# user.save()

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Custom related names for reverse relationships
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

