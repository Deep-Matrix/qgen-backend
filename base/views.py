from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .decorators import *
import jwt
from django.views.decorators.csrf import csrf_exempt


#auth
@api_view(['POST'])
def login(request):
	if request.method == 'POST':
		json_data = request.data
		email_id = json_data['email_id']
		password = json_data['password']
		# password hash
		users = User.objects.filter(email=email_id)
		if not users:
			return Response({'Message':"No user found in the database"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		user = users.first()
		if not user.password == password:
			return Response({'Message':"Wrong password"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		user_id = user.id
		token = get_token_from_object({'user_id':user_id},"_SECRET_KEY")
		user_serializer = UserSerializer([user],many=True)
		return Response({'Message':"User has been logged in",'user':user_serializer.data,'token':token},status=status.HTTP_200_OK)
	else:
		return Response({'Message':"Wrong method"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
	if request.method == 'POST':
		print("ANDAR AAGAYA")
		json_data = request.data
		email_id = json_data['email_id']
		password = json_data['password']
		username = json_data['username']
		# hash password
		users = User.objects.filter(email=email_id)
		if users:
			return Response({'Error':"Email already exists"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		new_user = User(email = email_id,username=username, password = password)
		new_user.save()
		return Response({'Message':"User has been created"},status=status.HTTP_200_OK)
	else:
		return Response({'Error':"Wrong method"},status=status.HTTP_400_BAD_REQUEST)


#get note
@api_view(['GET'])
@login_required
@csrf_exempt
def get_notes(request):
	notes = Notes.objects.all()
	serializer = NoteSerializer(notes,many=True)
	return JsonResponse(serializer.data,safe=False)

#add note
@api_view(['POST'])
@login_required
@csrf_exempt
def put_notes(request):
	if request.method == 'POST':
		json_data = request.data
		note_title = json_data['note_title']
		note_content = json_data['note_content']
		user_id = json_data['user_id']
		user_object = User.objects.get(id=user_id)
		note = Notes(user_id=user_object,note_title=note_title, content = note_content)
		note.save()
		return Response({'Message':"Note has been created"},status=status.HTTP_200_OK)

#delete note
@api_view(['POST'])
@login_required
@csrf_exempt
def delete_notes(request):
	if request.method == 'POST':
		json_data = request.data
		note_id = json_data['note_id']
		note = Notes(id=note_id).delete()
		return Response({'Message':"Note has been deleted"},status=status.HTTP_200_OK)


# {
# 	"email_id": "deepmatrix_user@gmail.com",
# 	"password" : "deep@123",
# 	"username" : "deepmatrix_user"
# }

# {
#     "Message": "User has been logged in",
#     "user": [
#         {
#             "id": 2,
#             "password": "deep@123",
#             "last_login": null,
#             "is_superuser": false,
#             "username": "deepmatrix_user",
#             "first_name": "",
#             "last_name": "",
#             "email": "deepmatrix_user@gmail.com",
#             "is_staff": false,
#             "is_active": true,
#             "date_joined": "2021-04-03T09:32:04.010753Z",
#             "groups": [],
#             "user_permissions": []
#         }
#     ],
#     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyfQ.l0ALEx_SFU71zFL-LEhGSBVJJ2-eUufEyCTjlVJqiEA"
# }


# {
# 	"note_title" : "My Note Title",
# 	"note_content" : "Note Content",
# 	"user_id" : "2"
# }