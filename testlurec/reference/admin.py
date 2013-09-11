from django.contrib import admin
from reference.models import Change, Collection, Event, Location, LocationCollection, LocationSighting, LocationMeasurement, LocationChange, Measurement, Organism, Parameter, People, Permit, Project, EventProject, Sighting


admin.site.register(Change)
admin.site.register(Collection)
admin.site.register(Event)
admin.site.register(Location)
admin.site.register(Measurement)
admin.site.register(Organism)
admin.site.register(Parameter)
admin.site.register(People)
admin.site.register(Permit)
admin.site.register(Project)
admin.site.register(EventProject)
admin.site.register(Sighting)
admin.site.register(LocationChange)
admin.site.register(LocationMeasurement)
admin.site.register(LocationSighting)
admin.site.register(LocationCollection)