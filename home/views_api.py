from lib2to3.pgen2 import token
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .helpers import generate_randomString, send_mail_to_user
from .models import Profile


class LoginView(APIView):

    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Somethin Went Wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['messagge'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key username not found')

            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user is None:
                response['message'] = 'Invalid username, user not found'
                raise Exception('Invalid Username')

            if not Profile.objects.filter(user = check_user).first().is_verified:
                response['message'] = 'Profile Not Verified'
                raise Exception('Prfile Not Verified')

            user_obj = authenticate(username = data.get('username'), password = data.get('password'))

            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = "Welcome"

            else:
                response['message'] = "Invalid password"
                raise Exception('Invalid Password')

        except Exception as e:
            print(e)
        
        return Response(response)

LoginView = LoginView.as_view()

class RegisterView(APIView):

    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Somethin Went Wrong'
        try:
            data = request.data

            if data.get('username') is None:
                response['messagge'] = 'key username not found'
                raise Exception('key username not found')
            
            if data.get('password') is None:
                response['message'] = 'key password not found'
                raise Exception('key username not found')

            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user:
                response['message'] = 'Username already taken'
                raise Exception('Username already taken')

            user_obj = User.objects.create(email = data.get('username'), username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_randomString(20)

            Profile.objects.create(user=user_obj, token = token)
            send_mail_to_user(token, data.get('username'))
            response['message'] = 'User Created'
            response['status'] = 200

            user_obj = authenticate(username = data.get('username'), password = data.get('password'))

            if user_obj:
                response['status'] = 200
                response['message'] = "Welcome"

            else:
                response['message'] = "Invalid password"
                raise Exception('Invalid Password')

        except Exception as e:
            print(e)
        
        return Response(response)

RegisterView = RegisterView.as_view()