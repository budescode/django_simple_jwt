from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
User= get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",            
            "password",
            "username",
            "id"
           
        ]
        read_only_fields = ['id']
    def create(self, data):
        password = data['password']
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return data 

    def validate_username(self, username):        
        if User.objects.filter(username__iexact = username).exists():
            raise serializers.ValidationError('A user with that username already exists.')
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid Login Details")
        return data

