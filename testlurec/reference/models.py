from django.db import models

#models automatically created by the import function of django

class Change(models.Model):
    objectid = models.IntegerField(unique=True)
    projectid = models.IntegerField()
    locationid = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255)
    justification = models.CharField(max_length=255)
    permanent = models.SmallIntegerField()
    chemicalapplication = models.SmallIntegerField()
    parameterid = models.IntegerField(null=True, blank=True)
    chemicalused = models.CharField(max_length=255, blank=True)
    chemicalquantity = models.DecimalField(null=True, max_digits=38, decimal_places=8, blank=True)
    chemicalunits = models.CharField(max_length=50, blank=True)
    areachange = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    personid = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'change'

class Collection(models.Model):
    objectid = models.IntegerField(unique=True)
    projectid = models.IntegerField()
    organismid = models.IntegerField()
    datecollect = models.DateTimeField()
    methodcollect = models.CharField(max_length=255, blank=True)
    stored = models.SmallIntegerField()
    storecollect = models.CharField(max_length=255, blank=True)
    locationid = models.IntegerField(null=True, blank=True)
    personid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'collection'

class Event(models.Model):
    eventtype = models.CharField(max_length=10)
    eventname = models.CharField(max_length=255)
    eventstartdate = models.DateTimeField()
    eventstarttime = models.DateTimeField(null=True, blank=True)
    eventenddate = models.DateTimeField()
    eventendtime = models.DateTimeField(null=True, blank=True)
    eventparticipants = models.IntegerField(null=True, blank=True)
    eventdescription = models.CharField(max_length=255, blank=True)
    personid = models.ForeignKey('AuthUser', db_column='personid')
    class Meta:
        db_table = 'event'
    def __unicode__(self):
        return self.eventname

class EventProject(models.Model):
    rid = models.IntegerField(unique=True)
    eventid = models.IntegerField(null=True, blank=True)
    project_objectid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'event_project'



class Location(models.Model):
    objectid = models.IntegerField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    pointid = models.IntegerField(null=True, blank=True)
    lineid = models.IntegerField(null=True, blank=True)
    areaid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'location'

class LocationChange(models.Model):
    rid = models.IntegerField(unique=True)
    locationid = models.IntegerField(null=True, blank=True)
    change_objectid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'location_change'

class LocationCollection(models.Model):
    rid = models.IntegerField(unique=True)
    locationid = models.IntegerField(null=True, blank=True)
    collection_objectid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'location_collection'

class LocationMeasurement(models.Model):
    rid = models.IntegerField(unique=True)
    locationid = models.IntegerField(null=True, blank=True)
    measurement_objectid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'location_measurement'

class LocationSighting(models.Model):
    rid = models.IntegerField(unique=True)
    locationid = models.IntegerField(null=True, blank=True)
    sighting_objectid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'location_sighting'


class Measurement(models.Model):
    objectid = models.IntegerField(unique=True)
    parameterid = models.IntegerField()
    projectid = models.IntegerField(null=True, blank=True)
    personid = models.IntegerField()
    locationid = models.IntegerField()
    mname = models.CharField(max_length=255)
    mmethod = models.CharField(max_length=255, blank=True)
    mquant = models.CharField(max_length=255)
    munits = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField()
    time = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    medium = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = 'measurement'

class Organism(models.Model):
    objectid = models.IntegerField(unique=True)
    organismname = models.CharField(max_length=255)
    family = models.CharField(max_length=255, blank=True)
    order_field = models.CharField(max_length=255, db_column='order_', blank=True) # Field renamed because it ended with '_'.
    class_field = models.CharField(max_length=255, db_column='class', blank=True) # Field renamed because it was a Python reserved word.
    phylum = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'organism'

class Parameter(models.Model):
    sciname = models.CharField(max_length=255, blank=True)
    commonname = models.CharField(max_length=50)
    casnumber = models.CharField(max_length=10, blank=True)
    epanumber = models.CharField(max_length=10, blank=True)
    class Meta:
        db_table = 'parameter'

class People(models.Model):
    objectid = models.IntegerField(unique=True)
    title = models.CharField(max_length=10)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    displayname = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=80)
    phonenumber = models.CharField(max_length=10, blank=True)
    affiliation = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'people'

class Permit(models.Model):
    permitstartdate = models.DateTimeField(null=True, blank=True)
    permitenddate = models.DateTimeField(null=True, blank=True)
    permitagency = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'permit'
    def __unicode__(self):
       return self.id

class Project(models.Model):
    projectname = models.CharField(max_length=100)
    projectdescription = models.CharField(max_length=255)
    projectobjective = models.CharField(max_length=255)
    eventid = models.ForeignKey('Event', db_column='eventid')
    permitid = models.ForeignKey('Permit', db_column='permitid', null=True)
    projectstartdate = models.DateTimeField()
    projectenddate = models.DateTimeField(null=True, blank=True)
    funded = models.SmallIntegerField()
    funder = models.CharField(max_length=255, blank=True)
    personid = models.ForeignKey('AuthUser', db_column='personid')
    class Meta:
        db_table = 'project'


class Sighting(models.Model):
    objectid = models.IntegerField(unique=True)
    personid = models.IntegerField()
    organismid = models.IntegerField()
    projectid = models.IntegerField(null=True, blank=True)
    locationid = models.IntegerField()
    number = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()
    time = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = 'sighting'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'
    def __unicode__(self):
        return self.first_name + " " + self.last_name