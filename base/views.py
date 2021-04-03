from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .decorators import *
import jwt
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import base64



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


#update note
@api_view(['POST'])
@login_required
@csrf_exempt
def update_notes(request):
	if request.method == 'POST':
		json_data = request.data
		note_id = json_data['note_id']
		note = Notes.objects.get(id = note_id)
		note.note_title = json_data['note_title']
		note.content = json_data['note_content']
		note.save()
		return Response({'Message':"Note has been updated"},status=status.HTTP_200_OK)
	

#get questions text from frontend pass to flask server then the questions genereated are passed to frontend again
@api_view(['POST'])
@login_required
def get_questions(request):
	if request.method == 'POST':
		json_data = request.data
		note_id = json_data['note_id']
		number_of_questions = json_data['number_of_questions']
		note = Notes.objects.get(id = note_id)
		#url for ml server
		ml_server_url = "localhost/questions/11"
		data = requests.post(ml_server_url, data = {'note_text': note.content, 'number_of_questions': number_of_questions})
		questions = json.loads(data.text)['questions']
		return Response({'Message':"recieved all questions from text", 'data': questions},status=status.HTTP_200_OK)


# get note from image, pass to ocr flask server get text, 
# send text to question generation flask, send this questions to frontend
@api_view(['POST'])
@login_required
def get_image_content(request):
	if request.method == 'POST':
		json_data = request.data
		number_of_questions = json_data['number_of_questions']
		img_data = request.FILES['file'].read()
		img_string = base64.b64encode(img_data)

		#url for ml server image to text
		ml_server_url = "localhost/questions/3"
		data = requests.post(ml_server_url, data = {'img_base64': img_string})
		note_text = json.loads(data.text)['image_text']

		#url for ml server question generation
		ml_server_url = "localhost/questions/14"
		data = requests.post(ml_server_url, data = {'note_text': note_text, 'number_of_questions': number_of_questions})
		questions = json.loads(data.text)['questions']
		return Response({'Message':"recieved all questions", 'data': questions},status=status.HTTP_200_OK)


#get note summary 
@api_view(['POST'])
@login_required
def get_summary(request):
	if request.method == 'POST':
		json_data = request.data
		note_id = json_data['note_id']
		note = Notes.objects.get(id = note_id)

		#url for ml server for summary
		ml_server_url = "localhost/summary"
		data = requests.post(ml_server_url, data = {'note_text': note.content})
		summary = json.loads(data.text)['summary']
		return Response({'Message':"recieved summary", 'data': summary},status=status.HTTP_200_OK)


# get note from image, pass to ocr flask server get text, 
# send text to summary generation flask, send this summary to frontend
@api_view(['POST'])
@login_required
def get_image_content_summary(request):
	if request.method == 'POST':
		img_data = request.FILES['file'].read()
		img_string = base64.b64encode(img_data)

		#url for ml server image to text
		ml_server_url = "localhost/questions"
		data = requests.post(ml_server_url, data = {'img_base64': img_string})
		note_text = json.loads(data.text)['image_text']

		#url for ml server image to text
		ml_server_url = "localhost/summary"
		data = requests.post(ml_server_url, data = {'note_text': note_text})
		summary = json.loads(data.text)['summary']
		return Response({'Message':"recieved summary from image", 'data': summary},status=status.HTTP_200_OK)


#get text from frontend, pass to flask server, then the flashcards generated are passed to frontend again
@api_view(['POST'])
@login_required
def get_flashcards(request):
	if request.method == 'POST':
		json_data = request.data
		note_id = json_data['note_id']
		number_of_flashcards = json_data['number_of_flashcards']
		note = Notes.objects.get(id = note_id)

		#url for ml server flashcards
		ml_server_url = "localhost/questions/1"
		data = requests.post(ml_server_url, data = {'note_text': note.content, 'number_of_flashcards': number_of_flashcards})
		flashcards = json.loads(data.text)['flashcards']
		return Response({'Message':"recieved all flashcards from text", 'data': flashcards},status=status.HTTP_200_OK)


# get note from image, pass to ocr flask server get text, 
# send text to flashcards generation flask, send this flashcardss to frontend
@api_view(['POST'])
@login_required
def get_image_content_flashcards(request):
	if request.method == 'POST':
		json_data = request.data
		number_of_flashcards = json_data['number_of_flashcards']

		img_data = request.FILES['file'].read()
		img_string = base64.b64encode(img_data)

		#url for ml server image to text
		ml_server_url = "localhost/questions"
		data = requests.post(ml_server_url, data = {'img_base64': img_string})
		note_text = json.loads(data.text)['image_text']

		#url for ml server flashcards generation
		ml_server_url = "localhost/questions/1"
		data = requests.post(ml_server_url, data = {'note_text': note_text, 'number_of_flashcards': number_of_flashcards})
		flashcards = json.loads(data.text)['flashcards']
		return Response({'Message':"recieved all flashcards", 'data': flashcards},status=status.HTTP_200_OK)



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


# {
# 	"note_id": "2",
#  	"note_title" : "Hello",
#  	"note_content" : "Note Content",
# 	"user_id" : "2"
# }

