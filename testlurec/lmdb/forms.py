from django import forms
from models import Parameter, Permit, Event, Project, People, Location, Organism, Measurement, Sighting, Collection, Change
from django.forms.extras.widgets import Select


class ParamForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    sciname = forms.CharField(max_length=100)
    commonname = forms.CharField()
    casnumber = forms.IntegerField()
    epanumber = forms.IntegerField()
    
    class Meta:
        model = Parameter
    
class PermitForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    permitstartdate = forms.DateTimeField()
    permitenddate = forms.DateTimeField()
    permitagency = forms.CharField()
    description = forms.CharField()
    
    class Meta:
        model = Permit
    
class EventForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
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
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    projectname = forms.CharField()
    projectdescription = forms.CharField()
    projectobjective = forms.CharField()
    locationid = forms.IntegerField()
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
    pointid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    lineid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    areaid = forms.IntegerField(widget=forms.TextInput(attrs={'readonly' : 'True'}),required=False)
    
    class Meta:
        model = Location

class OrganismForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    organismname = forms.CharField()
    family = forms.CharField(widget=Select(attrs={'disabled':'True'})) #last added line!!!!  
    order_field = forms.CharField(widget=Select(attrs={'disabled':'True'})) 
    class_field = forms.CharField(widget=Select(attrs={'disabled':'True'})) # Field renamed because it was a Python reserved word.
    phylum = forms.CharField(widget=Select(attrs={'disabled':'True'}))
    kingdom = forms.CharField(widget=Select( choices=(('',''),('Bacteria','Bacteria'),('Archaea','Archaea'),('Protista','Protista'),('Plantae','Plantae'),('Fungi','Fungi'),('Animalia','Animalia'))))
    genus = forms.CharField(widget=Select(attrs={'disabled':'True'}))
    species = forms.CharField(max_length=255)
    class Meta:
        model = Organism

class MeasurementForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    parameterid = forms.ModelChoiceField(queryset = Parameter.objects.all())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all(),required=False)
    personid = forms.ModelChoiceField(queryset = People.objects.all())
    locationid = forms.IntegerField(widget=forms.HiddenInput())
    mname = forms.CharField(max_length=255)
    mmethod = forms.CharField(max_length=255, required=False)
    mquant = forms.CharField(max_length=255)
    munits = forms.CharField(max_length=100, required=False)
    date = forms.DateTimeField()
    time = forms.DateTimeField(required=False)
    notes = forms.CharField(max_length=255, required=False)
    medium = forms.CharField(max_length=50, required=False)
    class Meta:
        model = Measurement
        
class SightingForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    personid = forms.ModelChoiceField(queryset = People.objects.all())
    organismid = forms.ModelChoiceField(queryset = Organism.objects.all())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all(),required=False)
    locationid = forms.IntegerField(widget=forms.HiddenInput())
    number = forms.IntegerField(required=False)
    date = forms.DateTimeField()
    time = forms.DateTimeField(required=False)
    notes = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Sighting

class CollectionForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all())
    organismid = forms.ModelChoiceField(queryset = Organism.objects.all())
    datecollect = forms.DateTimeField()
    methodcollect = forms.CharField(max_length=255)
    stored = forms.IntegerField()
    storecollect = forms.CharField(max_length=255)
    locationid = forms.IntegerField(widget=forms.HiddenInput())
    personid = forms.ModelChoiceField(queryset = People.objects.all(), required = False)
    class Meta:
        model = Collection
        
class ChangeForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all())
    locationid = forms.IntegerField(widget=forms.HiddenInput())
    description = forms.CharField(max_length=255)
    justification = forms.CharField(max_length=255)
    permanent = forms.IntegerField()
    chemicalapplication = forms.IntegerField()
    parameterid = forms.ModelChoiceField(queryset = Parameter.objects.all(), required=False)
    chemicalused = forms.CharField(max_length=255, required=False)
    chemicalquantity = forms.DecimalField(required=False, max_digits=38, decimal_places=8, )
    chemicalunits = forms.CharField(max_length=50, required=False)
    areachange = forms.CharField(max_length=50, required=False)
    date = forms.DateTimeField(required=False)
    personid = forms.ModelChoiceField(queryset = People.objects.all(), required = False)
    class Meta:
        model = Change