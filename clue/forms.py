# clue/forms.py
from django import forms
from .models import Teacher  # Import the Teacher model
from .models import Psychologist
from .models import Investigator



class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Teacher  # Link the form to the Teacher model
        fields = ['username', 'password']  # Fields to include in the form
        widgets = {
            'password': forms.PasswordInput(),  # Use a password input widget for security
        }

# forms.py

from django import forms
from .models import Crime

class PrincipalActionForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ['principal_action']
        widgets = {
            'principal_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'principal_action': 'Principal Action',
        }

from django import forms
from django.contrib.auth.hashers import make_password
from .models import Psychologist

class PsychologistRegistrationForm(forms.ModelForm):
    class Meta:
        model = Psychologist  # Link the form to the Psychologist model
        fields = ['username', 'password']  # Fields to include in the form
        widgets = {
            'password': forms.PasswordInput(),  # Use a password input widget for security
        }

    def save(self, commit=True):
        # Hash the password before saving the instance
        psychologist = super().save(commit=False)
        psychologist.password = make_password(self.cleaned_data['password'])
        if commit:
            psychologist.save()
        return psychologist
    

class InvestigatorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Investigator  # Link the form to the Psychologist model
        fields = ['username', 'password']  # Fields to include in the form
        widgets = {
            'password': forms.PasswordInput(),  # Use a password input widget for security
        }


from django import forms
from .models import crimeclue

class CrimeClueRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = crimeclue
        fields = ['username', 'password']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Optionally, you could add password hashing here, but if you want to store it as plain text, it will stay as is
        if commit:
            instance.save()
        return instance




