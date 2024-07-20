from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ParetoForm(forms.Form):
    complaint_type = forms.CharField(widget=forms.Textarea, label="Complaint Types (comma-separated)")
    number_of_complaints = forms.CharField(widget=forms.Textarea, label="Number of Complaints (comma-separated)")