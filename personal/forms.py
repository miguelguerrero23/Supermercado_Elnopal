from tkinter import Label
from django import forms
from personal.models import *
from  django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'    
        widgets={
            'dateBirth':forms.DateInput(format=(' %m/%d/%Y'),
                                    attrs={'class':'form-control',
                                            'placeholder':'Seleccione la fecha de nacimiento',
                                            'type':'date'})
        }
        
class customuserform(UserCreationForm):
    pass