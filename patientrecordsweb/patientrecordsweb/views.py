from django.shortcuts import render_to_response
from patientrecords.models import Doctor,Patient,Visit,CDT
from patientrecordsweb.forms import RegisterPatientForm,SaveCDTForm
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def newuser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/list/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", 
    {'form': form,},
    RequestContext(request))

@login_required
def registerpatient(request):
    if request.method == 'POST':
        form = RegisterPatientForm(request.POST)
        if form.is_valid():
            new_patient = form.save(commit=False)
            new_patient.doctor = request.user
            new_patient.save()
            return HttpResponseRedirect("/list/")
    else:
        form = RegisterPatientForm()
    return render_to_response("patient/register.html", 
    {'form': form,},
    RequestContext(request))

@login_required
def list(request):
    patients = Patient.objects.filter(doctor=request.user)
    return render_to_response("patient/list.html",locals())

@login_required
def details(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            return HttpResponse("Invalid query. Search query missing. Please click on patient from patient list to open their details")
        if len(q) > 11 or not q.isdigit():
            return HttpResponse("Invalid query. Search query format error. Please click on patient from patient list to open their details")
        
        patients = Patient.objects.filter(id=int(q))
        
        if len(patients) == 0:
            return HttpResponse("Invalid query. Please click on patient from patient list to open their details")
        elif len(patients) >1:
            return HttpResponse("Error: more than one patients returned for query")
        
        patient = patients[0]        
        if patient.doctor != request.user:
            return HttpResponse("You are unauthorised to view this patient. Please click on patient from patient list to open their details")
        
        request.session["patientid"] = q
        
        visits = Visit.objects.filter(patient=patient).order_by("-date")
        history = []
        for visit in visits:
            cdts = CDT.objects.filter(visit=visit)
            history.append({'cdts':cdts,'date':visit.date})
        return render_to_response('patient/details.html',locals(),RequestContext(request))
    else:
        return HttpResponse("Invalid query. Search query missing. Please click on patient from patient list to open their details")

@login_required
def newvisit(request):
    if "patientid" not in request.session:
        return HttpResponse("Request Expired. Please click on new visit on Patient Details page to create new Visit")
    patientid = request.session["patientid"]
    del request.session["patientid"]
    patients = Patient.objects.filter(id=patientid)
    patient=patients[0]
    visit = Visit(date=datetime.now(),patient=patient)
    visit.save()
    return render_to_response('visit/visitcreated.html',{'visit':visit})

@login_required
def addcdt(request):
    if 'q' not in request.GET:
        return HttpResponse("Invalid query. Visitid missing. Please click on edit visit from patinet details page")
    q = request.GET['q']
    if not q:
        return HttpResponse("Invalid query. Visitid missing. Please click on edit visit from patinet details page")
    if len(q) > 11 or not q.isdigit():
        return HttpResponse("Invalid query. Visitid format error. Please click on edit visit from patinet details page")    
    visits = Visit.objects.filter(id=int(q))        
    if len(visits) == 0:
        return HttpResponse("Invalid query. Please click on edit visit from patinet details page")
    visit = visits[0] 
    if visit.patient.doctor != request.user:
        return HttpResponse("You are unauthorised to view this patient. Please click on edit visit from patinet details page")
    
    if request.method == 'POST':
        form = SaveCDTForm(request.POST)
        if form.is_valid():
            new_cdt = form.save(commit=False)
            new_cdt.visit = visit
            new_cdt.save()
            return HttpResponseRedirect("/details/?q="+str(visit.patient.id))
    else:
        form = SaveCDTForm()
    return render_to_response("visit/addcdt.html", 
    {'form': form,},
    RequestContext(request))