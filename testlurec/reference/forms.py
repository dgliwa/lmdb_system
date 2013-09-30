from django import forms
from models import Parameter, Permit, Event, Project, People, Location, Organism
from django.forms.extras.widgets import SelectDateWidget


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
    permitstartdate = forms.DateTimeField(widget=SelectDateWidget())
    permitenddate = forms.DateTimeField(widget=SelectDateWidget())
    permitagency = forms.CharField()
    description = forms.CharField()
    
    class Meta:
        model = Permit
    
class EventForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput(), initial=Event.objects.all().order_by('-objectid')[0].objectid+1)
    eventname = forms.CharField()
    eventtype = forms.CharField()
    eventstartdate = forms.DateTimeField(widget=SelectDateWidget())
    eventenddate = forms.DateTimeField(widget=SelectDateWidget())
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
    projectstartdate = forms.DateTimeField(widget=SelectDateWidget())
    projectenddate = forms.DateTimeField(widget=SelectDateWidget())
    funded = forms.IntegerField()
    funder = forms.CharField()
    personid = forms.ModelChoiceField(queryset=People.objects.all())
    
    class Meta:
        model = Project
        
class LocationForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=255)
    pointid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    lineid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    areaid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    
    class Meta:
        model = Location

class OrganismForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    organismname = forms.CharField()
    family = forms.CharField(max_length=255)
    order_field = forms.CharField(max_length=255) # Field renamed because it ended with '_'.
    class_field = forms.CharField(max_length=255) # Field renamed because it was a Python reserved word.
    phylum = forms.CharField(max_length=255)
    kingdom = forms.CharField(max_length=255)
    genus = forms.CharField(max_length=255)
    species = forms.CharField(max_length=255)
    class Meta:
        model = Organism


