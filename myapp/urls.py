


from .views import simple_form, ItemAPIView

from django.conf import settings
from django.conf.urls.static import static
from .views import add_task, task_list
from .views import hello
from .views import signup, login,dashboard
from django.urls import path
from .views import tutorial_list, tutorial_detail, tutorial_list_published

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('hello/', simple_form, name='simple_form'),
    path('add-task/', add_task, name='add_task'),
    path('tasks/', task_list, name='task_list'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('tutorials/', tutorial_list, name='tutorial-list'),
    path('tutorials/<int:pk>/', tutorial_detail, name='tutorial-detail'),
    path('tutorials/published/', tutorial_list_published, name='tutorial-list-published'),
    path('item/',ItemAPIView.as_view(),name = 'item'),
    # Add other paths as needed
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




