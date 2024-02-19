from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Note, SharedNote, NoteVersionHistory
from .serializers import NoteSerializer, SharedNoteSerializer, NoteUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token





@api_view(['POST'])
def user_registration(request):
    print(request.data,'111111111111111')
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registration successful"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": {"id": user.id, "username": user.username, "email": user.email}}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_note(request):
    print(request.data,'33333333333')
    serializer = NoteSerializer(data=request.data)
    print("5555555555555555555")
    if serializer.is_valid():
        print("2222222222222222")
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note(request, id):
    try:
        note = Note.objects.get(pk=id)
        if request.user == note.owner or note.sharednote_set.filter(shared_with=request.user).exists():
            serializer = NoteSerializer(note)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not authorized to view this note."}, status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response({"message": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def share_note(request):
    serializer = SharedNoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Note shared successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_note(request, id):
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return Response({"message": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != note.owner and not note.sharednote_set.filter(shared_with=request.user).exists():
        return Response({"message": "You are not authorized to update this note."}, status=status.HTTP_403_FORBIDDEN)

    serializer = NoteUpdateSerializer(note, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        NoteVersionHistory.objects.create(note=note, user=request.user, changes=request.data['content'])
        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_note_version_history(request, id):
    try:
        note = Note.objects.get(pk=id)
    except Note.DoesNotExist:
        return Response({"message": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != note.owner and not note.sharednote_set.filter(shared_with=request.user).exists():
        return Response({"message": "You are not authorized to view the version history of this note."}, status=status.HTTP_403_FORBIDDEN)

    version_history = NoteVersionHistory.objects.filter(note=note).order_by('timestamp')
    data = [{"timestamp": history.timestamp, "user": history.user.username, "changes": history.changes} for history in version_history]
    return Response(data, status=status.HTTP_200_OK)

