from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    doctor = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name

class Visit(models.Model):
    date = models.DateField()
    patient = models.ForeignKey(Patient)

class CDT(models.Model):
    CONDITION_CHOICES = (
        ('1', 'Condition 1'),
        ('2', 'Condition 2'),
        ('3', 'Condition 3'),
        ('4', 'Condition 4'),
        ('5', 'Condition 5'),
        ('6', 'Condition 6'),
        ('7', 'Condition 7'),
        ('8', 'Condition 8'),
        ('9', 'Condition 9'),
        ('10', 'Condition 10'),
    )
    condition = models.CharField(max_length=11, choices=CONDITION_CHOICES)
    DIAGNOSIS_CHOICES = (
        ('1', 'Diagnosis 1'),
        ('2', 'Diagnosis 2'),
        ('3', 'Diagnosis 3'),
        ('4', 'Diagnosis 4'),
        ('5', 'Diagnosis 5'),
        ('6', 'Diagnosis 6'),
        ('7', 'Diagnosis 7'),
        ('8', 'Diagnosis 8'),
        ('9', 'Diagnosis 9'),
        ('10', 'Diagnosis 10'),
    )
    diagnosis = models.CharField(max_length=11, choices=DIAGNOSIS_CHOICES)
    TREATMENT_CHOICES = (
        ('1', 'Treatment 1'),
        ('2', 'Treatment 2'),
        ('3', 'Treatment 3'),
        ('4', 'Treatment 4'),
        ('5', 'Treatment 5'),
        ('6', 'Treatment 6'),
        ('7', 'Treatment 7'),
        ('8', 'Treatment 8'),
        ('9', 'Treatment 9'),
        ('10', 'Treatment 10'),
    )
    treatment = models.CharField(max_length=11, choices=TREATMENT_CHOICES)
    visit = models.ForeignKey(Visit)