from django.shortcuts import render
from helpers.helpers.response import custom_error_msg
from .serializers import LoginSerializer, UserSerializer
from rest_framework import generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(generics.CreateAPIView):    
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.validated_data.pop('password')
            data = {'message':'Registration Successful', 'status':True, 'data':serializer.validated_data}
            return Response(serializer.validated_data, status=HTTP_201_CREATED)
        else:
            data = {"message": custom_error_msg(serializer.errors), 'status':False, 'data':{}}
            return Response(data, status=HTTP_400_BAD_REQUEST)

class LoginUserView(generics.CreateAPIView):    
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            username = serializer.validated_data["username"]

            user = authenticate(username=username, password=password) 
            user_serialized = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
             
            userdetails = user_serialized.data
            userdetails["access_token"] = str(access)
            userdetails["refresh"] = str(refresh)            
            data = {'message':'Login Successful', 'status':True, 'data':userdetails}
            return Response(data, status=HTTP_200_OK)           

        else:            
            data = {"message": custom_error_msg(serializer.errors), 'status':False, 'data':{}}
            return Response(data, status=HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]   
    def get(self, request, format=None):
        user = self.request.user
        user_serialized = UserSerializer(user)
        data = {'message':'Successful', 'status':True, 'data':user_serialized.data}
        return Response(data)
