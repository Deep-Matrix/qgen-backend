from django.urls import path,include
from . import views 
urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('get_notes',views.get_notes,name='get_notes'),
    path('put_note',views.put_notes,name='put_notes'),
    path('delete_note',views.put_notes,name='delete_notes'),
]
