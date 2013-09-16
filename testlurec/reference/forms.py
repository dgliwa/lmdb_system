from django import forms
from models import AuthUser, Parameter, Permit, Event, Project

import random

class ParamForm(forms.ModelForm):
    sciname = forms.CharField(max_length=100)
    commonname = forms.CharField()
    casnumber = forms.IntegerField()
    epanumber = forms.IntegerField()
    
    class Meta:
        model = Parameter
    
class PermitForm(forms.ModelForm):
    permitstartdate = forms.DateTimeField()
    permitenddate = forms.DateTimeField()
    permitagency = forms.CharField()
    description = forms.CharField()
    
    class Meta:
        model = Permit
    
class EventForm(forms.ModelForm):
    eventname = forms.CharField()
    eventtype = forms.CharField()
    eventstartdate = forms.DateTimeField()
    eventenddate = forms.DateTimeField()
    eventparticipants = forms.IntegerField()
    eventdescription = forms.CharField()
    personid = forms.ModelChoiceField(queryset=AuthUser.objects.all())
    
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
    personid = forms.ModelChoiceField(queryset=AuthUser.objects.all())
    
    class Meta:
        model = Project