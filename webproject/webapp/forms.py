from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Importar o modelo de usuário personalizado


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Especificar o modelo CustomUser
        fields = ('username', 'email', 'password1', 'password2')  # Campos que você deseja no formulário