from django.urls import path,include
from . import views 
urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('get_notes',views.get_notes,name='get_notes'),
    path('put_note',views.put_notes,name='put_notes'),
    path('delete_note',views.delete_notes,name='delete_notes'),
    path('update_note',views.update_notes,name='update_notes'),
    path('get_questions',views.get_questions,name='get_questions'),
    path('get_image_content',views.get_image_content,name='get_image_content'),
]
