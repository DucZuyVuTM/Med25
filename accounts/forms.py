from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class PatientRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 
                  'phone', 'address', 'password1', 'password2')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'  # Get default role
        if commit:
            user.save()
        return user
