from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import FirstLoginForm, NoteForm, NoteUpdateForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Note
from django.shortcuts import get_object_or_404


def login_view(request):
    """
    login view path is empty ""
    """
    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')
        form = FirstLoginForm(data=request.POST)
        if form.is_valid():
            if student_number is not None and password is not None:
                user = authenticate(request, username=student_number, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'your username or password is incorrect. ')

    else:
        form = FirstLoginForm()
    return render(request, 'first_login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def send_note(request):
    """
    logged-in users send notes to other users using NoteForm
    logged-in user is saved as sender and the person who is chosen in the form is saved as recipient
    if it is saved it shows a success message
    """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.sender = request.user
            note.save()
            messages.success(request, 'You have sent your note.You can update it later.')
    else:
        form = NoteForm()
    return render(request, 'send_note.html', {'form': form})


@login_required()
def update_note(request, id):
    """
    logged-in user can update sent notes here using note update form which includes old written notes
    if it is saved it shows a success message
    """
    instance = get_object_or_404(Note, id=id)
    if request.method == 'POST':
        form = NoteUpdateForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have updated your note.')
    else:
        form = NoteUpdateForm(instance=instance)
    return render(request, 'note_update.html', {'form': form, 'note': instance})


@login_required
def note_action(request, id, action):
    """
    logged-in user can determine statuses of received notes as 'approve' or 'disapprove'
    """
    note = get_object_or_404(Note, id=id)
    if action == 'approve':
        note.status = 'approved'
    elif action == 'disapprove':
        note.status = 'disapproved'

    note.save()
    return redirect('status_change', id=id)


def status_change(request):
    return render(request, 'status_change.html')


@login_required
def note_detail(request, id):
    """
    this function is used for showing the action that logged-in users have made on status situation
    in the html template.
    """
    note = get_object_or_404(Note, id=id)
    context = {
        'status': note.status
    }
    return render(request,'status_change.html', context)


@login_required
def user_notes(request):
    """
    logged-in users can view the notes they have written and update it if they want
    """
    notes = Note.objects.filter(sender=request.user)
    return render(request, 'user_notes.html', {'notes': notes})


@login_required
def receive_notes(request):
    """
    logged-in users can view the notes written to them
    if they disapproved the notes using note_action function
    the note disappears from receive_notes.html template
    """
    notes = Note.objects.filter(recipient=request.user).exclude(status='disapproved')
    return render(request, 'receive_notes.html', {'notes': notes})


@login_required
def disapproved_notes(request):
    """
    logged-in users can view the notes that they disapproved
    if they change their minds they can approve it again using disapproved_notes.html template
    """
    notes = Note.objects.filter(recipient=request.user, status='disapproved')
    return render(request, 'disapproved_notes.html', {'notes': notes})


@login_required()
def password_change_view(request):
    """
    it is a custom password change view
    actually I was lazy to customize default password change form, so I just write it again:)
    the new password does not require special characters
    """
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        password_confirm = request.POST.get('password_confirm')
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            user = request.user
            if user.check_password(old_password):
                if old_password != new_password:
                    if len(new_password) < 8:
                        messages.error(request, 'new password cannot be less then 8 characters. ')
                    else:
                        if new_password == password_confirm:
                            user.set_password(new_password)
                            user.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Your password was successfuly updated. Please login with your new password')
                            return render(request, 'first_login.html')
                        else:
                            messages.error(request, 'new password and password confirm do not match ')
                else:
                    messages.error(request, 'old password and new password can not be the same')
            else:
                messages.error(request, 'existed password is wrong')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def password_change_success_view(request):
    return render(request, 'change_success.html')


def user_logout(request):
    """
    dümdüz logout bra ne anlatıyım yani
    """
    logout(request)
    return redirect('login_view')













