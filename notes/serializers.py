from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, SharedNote, NoteVersionHistory
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or email):
            raise serializers.ValidationError("Username or email is required for login.")

        user = authenticate(username=username, email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username/email or password.")

        attrs['user'] = user
        return attrs
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = ['note', 'shared_with']

class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['content', 'title']
        