from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to every field without hand-writing each input
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'current_skills', 'interests', 'career_goal',
            'experience_level', 'weekly_study_hours', 'preferred_platform',
        ]
        widgets = {
            'current_skills': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Python, SQL, Excel'}),
            'interests': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. AI, Web Development'}),
            'career_goal': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Data Scientist'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'weekly_study_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'preferred_platform': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'e.g. Coursera'}),
        }
