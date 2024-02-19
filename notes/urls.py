from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.user_registration),
    path('login/', views.user_login),
    path('create/', views.create_note),
    path('<int:id>/', views.get_note),
    path('share/', views.share_note),
    path('update/<int:id>/', views.update_note),
    path('version-history/<int:id>/', views.get_note_version_history),
    
]
