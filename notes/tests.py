from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note, SharedNote, NoteVersionHistory

class NoteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_note(self):
        data = {'title': 'Test Note', 'content': 'This is a test note content.'}
        response = self.client.post('/notes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        response = self.client.get(f'/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        data = {'note': note.id, 'shared_with': [self.user.id]}
        response = self.client.post('/notes/share/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_note(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        data = {'title': 'Updated Test Note', 'content': 'Updated note content.'}
        response = self.client.put(f'/notes/update/{note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_note_version_history(self):
        note = Note.objects.create(title='Test Note', content='This is a test note content.', owner=self.user)
        NoteVersionHistory.objects.create(note=note, user=self.user, changes='Initial note creation.')
        response = self.client.get(f'/notes/version-history/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newuserpassword'}
        response = self.client.post(f'/notes/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(f'/notes/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
