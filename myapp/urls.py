from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path('home/', views.home, name='home'),
    path("user_logout", views.user_logout, name="user_logout"),
    path('change-password/', views.password_change_view, name="password_change_view"),
    path('send_note/', views.send_note, name='send_note'),
    path('received-notes/', views.receive_notes, name='receive_notes'),
    path('user-notes', views.user_notes, name='user_notes'),
    path('update_note/<int:id>/', views.update_note, name='update_note'),
    path('note_action/<int:id>/<str:action>/', views.note_action, name='note_action'),
    path('status/<int:id>/', views.note_detail, name='status_change'),
    path('password-change-success/', views.password_change_success_view, name='password_change_success'),
    path('disapproved_notes/', views.disapproved_notes, name='disapproved_notes')

]