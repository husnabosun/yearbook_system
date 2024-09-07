from django import forms
from .models import Note, CustomUser
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget


class FirstLoginForm(forms.Form):
    student_number = forms.CharField(label='username/student_number', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())


class NoteForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_active=True, is_staff=False, is_superuser=False),
        empty_label="Select recipient",
        widget=Select2Widget(attrs={'class': 'form-control'})
    )
    text = forms.CharField(label='Write your note', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Hey Sandra...'}))

    class Meta:
        model = Note
        fields = ['recipient', 'text']

    def clean_text(self):
        text = self.cleaned_data['text']
        word_count = len(text.split())
        if word_count > 200:
            raise ValidationError('Text exceeds 200 words.')
        return text


class NoteUpdateForm(forms.ModelForm):
    text = forms.CharField(label='Write your note', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Hey Sandra...'}))

    class Meta:
        model = Note
        fields = ['text']



