from django import forms
from models import Parameter, Permit, Event, Project, People, Location
from django.contrib.auth.models import User

import random

class ParamForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput(), initial=Parameter.objects.all().order_by('-objectid')[0].objectid+1)
    sciname = forms.CharField(max_length=100)
    commonname = forms.CharField()
    casnumber = forms.IntegerField()
    epanumber = forms.IntegerField()
    
    class Meta:
        model = Parameter
    
class PermitForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput(), initial=Permit.objects.all().order_by('-objectid')[0].objectid+1)
    permitstartdate = forms.DateTimeField()
    permitenddate = forms.DateTimeField()
    permitagency = forms.CharField()
    description = forms.CharField()
    
    class Meta:
        model = Permit
    
class EventForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput(), initial=Event.objects.all().order_by('-objectid')[0].objectid+1)
    eventname = forms.CharField()
    eventtype = forms.CharField()
    eventstartdate = forms.DateTimeField()
    eventenddate = forms.DateTimeField()
    eventparticipants = forms.IntegerField()
    eventdescription = forms.CharField()
    personid = forms.ModelChoiceField(queryset=People.objects.all())
    
    class Meta:
        model = Event
        
class ProjectForm(forms.ModelForm):
    projectname = forms.CharField()
    projectdescription = forms.CharField()
    projectobjective = forms.CharField()
    eventid = forms.ModelChoiceField(queryset=Event.objects.all())
    permitid = forms.ModelChoiceField(queryset=Permit.objects.all())
    projectstartdate = forms.DateTimeField()
    projectenddate = forms.DateTimeField()
    funded = forms.IntegerField()
    funder = forms.CharField()
    personid = forms.ModelChoiceField(queryset=People.objects.all())
    
    class Meta:
        model = Project
        
class LocationForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255)
    pointid = forms.IntegerField()
    lineid = forms.IntegerField()
    areaid = forms.IntegerField()
    
    class Meta:
        model = Location

