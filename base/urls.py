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
    path('get_summary',views.get_summary,name='get_summary'),
    path('get_image_content_summary',views.get_image_content_summary,name='get_image_content_summary'),
    path('get_flashcards',views.get_flashcards,name='get_flashcards'),
    path('get_image_content_flashcards',views.get_image_content_flashcards,name='get_image_content_flashcards'),
]
