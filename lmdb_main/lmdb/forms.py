from django import forms
from models import Parameter, Permit, Event, Project, People, Location, Organism, Measurement, Sighting, Collection, Change
from django.forms.extras.widgets import Select
from django.contrib.auth.models import User
from validators import *
from lmdb.models import *



class ParamForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    sciname = forms.CharField(max_length=100)
    commonname = forms.CharField()
    casnumber = forms.IntegerField()
    epanumber = forms.IntegerField()
    category = forms.CharField(widget=Select( choices=(('Chemical','Chemical'),('Physical','Physical'),('Spatial','Spatial'),('Temporal','Temporal'),('General','General'))))
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
    eventid = forms.ModelChoiceField(queryset=Event.objects.all())
    permitid = forms.ModelChoiceField(queryset=Permit.objects.all())
    projectstartdate = forms.DateTimeField()
    projectenddate = forms.DateTimeField()
    funded = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))))
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
    wetland_designation = forms.CharField(max_length=10, required=False)
    cvalue = forms.IntegerField(required=False)
    introduced = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))), required=False)
    class Meta:
        model = Organism

class EditOrganismForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    organismname = forms.CharField()
    family = forms.CharField(widget=Select()) #last added line!!!!  
    order_field = forms.CharField(widget=Select()) 
    class_field = forms.CharField(widget=Select()) # Field renamed because it was a Python reserved word.
    phylum = forms.CharField(widget=Select())
    kingdom = forms.CharField(widget=Select())
    genus = forms.CharField(widget=Select())
    species = forms.CharField(max_length=255)
    wetland_designation = forms.CharField(max_length=10, required=False)
    cvalue = forms.IntegerField(required=False)
    introduced = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))), required=False)
    class Meta:
        model = Organism
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']
        #print instance
        super(EditOrganismForm, self).__init__(*args, **kwargs)
        self.fields['objectid'] = forms.IntegerField(widget=forms.HiddenInput(),initial=instance.objectid)
        self.fields['organismname'] = forms.CharField(initial=instance.organismname)
        self.fields['kingdom']= forms.CharField(initial=instance.kingdom,widget=Select(choices=(('',''),('Bacteria','Bacteria'),('Archaea','Archaea'),('Protista','Protista'),('Plantae','Plantae'),('Fungi','Fungi'),('Animalia','Animalia'))))
        phylae = Organism.objects.filter(kingdom=instance.kingdom).values('phylum').distinct()
        choices = []
        for ph in phylae:
            choices.append((ph['phylum'],ph['phylum']))
        tuple(choices)
        self.fields['phylum'] = forms.CharField(initial=instance.phylum, widget=Select(choices=choices))
        class_fields = Organism.objects.filter(phylum=instance.phylum).values('class_field').distinct()
        choices = []
        for cl in class_fields:
            choices.append((cl['class_field'],cl['class_field']))
        tuple(choices)
        self.fields['class_field'] = forms.CharField(initial=instance.class_field, widget=Select(choices=choices))
        order_fields = Organism.objects.filter(class_field=instance.class_field).values('order_field').distinct()
        choices = []
        for order in order_fields:
            choices.append((order['order_field'],order['order_field']))
        tuple(choices)
        self.fields['order_field'] = forms.CharField(initial=instance.order_field, widget=Select(choices=choices))
        families = Organism.objects.filter(class_field=instance.class_field).values('family').distinct()  
        choices = []
        for fam in families:
            choices.append((fam['family'],fam['family']))
        tuple(choices)
        self.fields['family'] = forms.CharField(initial=instance.family, widget=Select(choices=choices))
        genera = Organism.objects.filter(family=instance.family).values('genus').distinct()
        choices = []
        for g in genera:
            choices.append((g['genus'],g['genus']))
        tuple(choices)
        self.fields['genus'] = forms.CharField(initial=instance.genus, widget=Select(choices=choices))
        self.fields['species'] = forms.CharField(initial=instance.species, max_length=255)
        self.fields['wetland_designation'] = forms.CharField(initial=instance.wetland_designation, max_length=10, required=False)
        self.fields['cvalue'] = cvalue = forms.IntegerField(initial=instance.cvalue, required=False)
        self.fields['introduced'] = forms.IntegerField(initial=instance.introduced, widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))), required=False)
        # peopleproject = PeopleProject.objects.filter(personid=userid)
        # projects = []
        # for pp in peopleproject:
        #     projects.append(pp.projectid.objectid)
        # self.fields['projectid'].queryset = Project.objects.filter(objectid__in = projects)

class MeasurementForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    parameterid = forms.ModelChoiceField(queryset = Parameter.objects.all(), widget=forms.Select(attrs={'class':'paramfield'}))
    projectid = forms.ModelChoiceField(queryset = Project.objects.all(),required=False)
    personid = forms.ModelChoiceField(queryset = People.objects.all())
    locationid = forms.IntegerField(widget=forms.TextInput(attrs={"readonly" : "true"}))
    mname = forms.CharField(max_length=255)
    mmethod = forms.CharField(max_length=255, required=False)
    mquant = forms.CharField(max_length=255)
    munits = forms.CharField(max_length=100, required=False)
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datefield'}))
    time = forms.DateTimeField(required=False)
    notes = forms.CharField(max_length=255, required=False)
    medium = forms.CharField(max_length=50, required=False)
    class Meta:
        model = Measurement
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        super(MeasurementForm, self).__init__(*args, **kwargs)
        peopleproject = PeopleProject.objects.filter(personid=userid)
        projects = []
        for pp in peopleproject:
            projects.append(pp.projectid.objectid)
        self.fields['projectid'].queryset = Project.objects.filter(objectid__in = projects)
        
class SightingForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    personid = forms.ModelChoiceField(queryset = People.objects.all())
    organismid = forms.ModelChoiceField(queryset = Organism.objects.all(), widget=forms.Select(attrs={'class':'organismfield'}))
    projectid = forms.ModelChoiceField(queryset = Project.objects.all(),required=False)
    locationid = forms.IntegerField(widget=forms.TextInput(attrs={"readonly" : "true"}))
    number = forms.IntegerField(required=False)
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datefield'}))
    time = forms.DateTimeField(required = False, widget=forms.TextInput(attrs={'class':'datefield'}))
    notes = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Sighting
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        super(SightingForm, self).__init__(*args, **kwargs)
        peopleproject = PeopleProject.objects.filter(personid=userid)
        projects = []
        for pp in peopleproject:
            projects.append(pp.projectid.objectid)
        self.fields['projectid'].queryset = Project.objects.filter(objectid__in = projects)

class CollectionForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all())
    organismid = forms.ModelChoiceField(queryset = Organism.objects.all(), widget=forms.Select(attrs={'class':'organismfield'}))
    datecollect = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datefield'}))
    methodcollect = forms.CharField(max_length=255)
    stored = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))))
    storecollect = forms.CharField(max_length=255)
    locationid = forms.IntegerField(widget=forms.TextInput(attrs={"readonly" : "true"}))
    personid = forms.ModelChoiceField(queryset = People.objects.all(), required = False)
    class Meta:
        model = Collection
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        super(CollectionForm, self).__init__(*args, **kwargs)
        peopleproject = PeopleProject.objects.filter(personid=userid)
        projects = []
        for pp in peopleproject:
            projects.append(pp.projectid.objectid)
        self.fields['projectid'].queryset = Project.objects.filter(objectid__in = projects)
        
class ChangeForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    projectid = forms.ModelChoiceField(queryset = Project.objects.all())
    locationid = forms.IntegerField(widget=forms.TextInput(attrs={"readonly" : "true"}))
    description = forms.CharField(max_length=255)
    justification = forms.CharField(max_length=255)
    permanent = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))))
    chemicalapplication = forms.IntegerField(widget=forms.RadioSelect(choices=((1,'Yes'),(0,'No'))))
    parameterid = forms.ModelChoiceField(queryset = Parameter.objects.all(), required=False, widget=forms.Select(attrs={'class':'paramfield'}))
    chemicalused = forms.CharField(max_length=255, required=False)
    chemicalquantity = forms.DecimalField(required=False, max_digits=38, decimal_places=8, )
    chemicalunits = forms.CharField(max_length=50, required=False)
    areachange = forms.CharField(max_length=50, required=False)
    date = forms.DateTimeField(required=False, widget=forms.TextInput(attrs={'class':'datefield'}))
    personid = forms.ModelChoiceField(queryset = People.objects.all(), required = False)
    class Meta:
        model = Change
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('user')
        super(ChangeForm, self).__init__(*args, **kwargs)
        peopleproject = PeopleProject.objects.filter(personid=userid)
        projects = []
        for pp in peopleproject:
            projects.append(pp.projectid.objectid)
        self.fields['projectid'].queryset = Project.objects.filter(objectid__in = projects)
        
class PeopleForm(forms.ModelForm):
    objectid = forms.IntegerField(widget=forms.HiddenInput())
    title = forms.CharField(max_length=10, required=False)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'True'}), max_length=50)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'True'}), max_length=50)
    displayname = forms.CharField(max_length=50, required=False)
    email = forms.CharField(max_length=80)
    phonenumber = forms.CharField(max_length=10, required=False, validators=[is_num])
    affiliation = forms.CharField(max_length=100, required=False)
    position = forms.CharField(max_length=50, required=False)
    department = forms.CharField(max_length=50, required=False)
    password = forms.CharField(max_length=100, required=False)
    class Meta:
        model = People   