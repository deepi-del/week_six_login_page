from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the email field read-only if an instance exists (editing mode)
        if self.instance and self.instance.pk:
            self.fields['email'].disabled = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Skip uniqueness validation if the email field is read-only
        if not self.fields['email'].disabled and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
