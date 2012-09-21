from django import forms
from patientrecords.models import Patient,CDT
from django.forms import ModelForm

class RegisterPatientForm(ModelForm):
     class Meta:
         model = Patient
         exclude = ('doctor',)

class SaveCDTForm(ModelForm):
    class Meta:
        model = CDT
        exclude = ('visit',)