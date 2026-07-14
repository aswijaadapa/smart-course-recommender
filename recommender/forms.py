from django import forms


class RecommendationForm(forms.Form):
    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    skills = forms.CharField(
        label="Current Skills",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Excel'}),
        required=False,
    )
    interests = forms.CharField(
        label="Interests",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Science, AI'}),
        required=False,
    )
    career_goal = forms.CharField(
        label="Career Goal",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Scientist'}),
        required=True,
    )
    experience_level = forms.ChoiceField(
        label="Experience Level",
        choices=EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    weekly_study_hours = forms.IntegerField(
        label="Weekly Study Hours",
        min_value=1, max_value=80,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    preferred_platform = forms.CharField(
        label="Preferred Platform",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Coursera, Udemy'}),
        required=False,
    )
