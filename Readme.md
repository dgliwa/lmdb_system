# Welcome to the LUREC LMDB System Repository

![Map Image](https://lmdb.luc.edu/static/images/lurecMap1.jpg)

Introduction to the System
--------------------------
The purpose of the LMDB System is to provide an application where users can submit data recorded on LUREC's grounds.  This data falls in to four categories:

* Changes
* Collections
* Measurements
* Sightings

The inputted data provides information on known **parameters** and **organisms** on the LUREC grounds.  The recordings on plotted on a map of LUREC using a spatial database.

Tools
-----------------

The **LMDB System** was developed using two main tools:

* [Django](https://www.djangoproject.com/)
* [ArcGIS](https://developers.arcgis.com/javascript/)

Great tutorials can be found on those websites to supplement the information on this Readme.

Django Code
------------------
There are three main sections of the code:

* The LMDB (reference) section
* The data input section
* The reporting section

These sections are writted as separate django 'apps', and are in their own directory of the system.

The directory that ties these 'apps' together is the **lmdb_main** directory. In here you will find the settings.py directory, which has the settings for static files, the databases, and the installed django apps.

---
Django is a Model View Controller (or as some would call it, Model View Template) framework.  It is implemented by a url router directing an http request to what django calls views, which then render templates to be sent back as a response.

The lmdb_main urls.py router handles the major routing, and sends specific requests to the django app urls.py files.

```
urlpatterns = patterns('',
	...
     url(r'^', include('lmdb.urls', namespace='lmdb')),
     url(r'^data/', include('data.urls', namespace='data')),
     url(r'^reporting/', include('reporting.urls', namespace='reporting')),
     ...
)
```
As you can see, specific urls such as those starting with 'data/' or 'reporting/' are routed to the reporting and data apps.

---
Each app has its own **views.py** file.  The functions in the views.py file do various activities, such as save, update, delete, or get models, and render them in a template before sending a response.
Here is an example views function being called from the LMDB urls.py file:

    url(r'^reference/organisms/$', views.organisms, name='organisms'),


```
@login_required(login_url='/login/')
@user_uploaded
def organisms(request):
    organisms = Organism.objects.all().order_by('organismname')
    template = loader.get_template('lmdb/organisms.html')
    context = RequestContext( request, {
        'organisms' : organisms,
    })
    return HttpResponse(template.render(context))
 ```

The url router called the organisms function.  The organisms function then queried all the Organisms (a django model) in the database, and rendered them in a response to the client.  **Django models** are easily defined and related to the database.  This makes for easy querying.  All the models for the LMDB application are in the LMDB directory.  The Organism model is defined below, as an example:

```
class Organism(models.Model):
    objectid = models.IntegerField(primary_key=True,unique=True)
    organismname = models.CharField(max_length=255)
    family = models.CharField(max_length=255, blank=True)
    order_field = models.CharField(max_length=255, db_column='order_', blank=True) # Field renamed because it ended with '_'.
    class_field = models.CharField(max_length=255, db_column='class', blank=True) # Field renamed because it was a Python reserved word.
    phylum = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)
    wetland_designation = models.CharField(max_length=10, db_column='wld_1', null=True)
    cvalue = models.IntegerField(null=True)
    introduced = models.SmallIntegerField(null=True)
    class Meta:
        db_table = 'organism'
    def __unicode__(self):
        return self.organismname
```

Each variable in the Organism model is associated with a column in the database.  Upon retrieval from the database, those fields are populated and easily accessed from the model.

---
The final part of the django MVC process is the rendering of a template.  Django has a special syntax that allows for django variables to be read into an html page.  Following from the organisms example above, [here is the organisms.html template that will be rendered with organism variables](https://github.com/dgliwa/lmdb_system/blob/master/lmdb_main/lmdb/templates/lmdb/organisms.html).  The `{% ... %}` and `{{ ... }}` syntax tells the template engine to read django variables.

Maps
---
ArcGIS javascript is used to graphically display the map layers of the database, and to add locations to the ArcGIS database.  The maps are loaded on several of the pages, most of them being the data input pages.  The javascript for these maps is currently messy, and I am working to improve readability.  However, the map javascript files are in the lmdb templates directory, and are imported using the django import and extend syntax.  There are three main map templates.

Currently, the data creation pages use the mapbase.html file.  The data detail pages use the mapdetail.html file. The overall data list pages extend the tablebase.html file.  The creation and detail pages use the "include" syntax which is as follows: `{% include 'mapbase.html' %}`. This syntax simply imports the code from the mapbase or mapdetail file and inserts it where the include statement is.

The data list pages use the extend syntax, which provides a skeleton with blocks to be filled.  [Here is an example of the a data list page extending the tablebase.html file](https://github.com/dgliwa/lmdb_system/blob/master/lmdb_main/data/templates/data/createChange.html).  The `{% block %} ... {% endblock %}` syntax allows each page that extends the tablebase.html file to put custom code inside it.

ArcGIS Code
---
The javascript for the displaying the maps creates several layers on a basemap and populates the maps with the data for each layer.  The code works in a few logical steps:

* David worked to create a secure service for the LMDB maps, so the code must first acquire a token.  This is done by the signIn function.

```
function signIn() {
        console.log('signing in')
      //dojo.byId("signInStatus").innerHTML = "Creating token...";

      // Get token from the ArcGIS Server Token Service.
      //
      esri.request({
        url: "https://jeez.etl.luc.edu/arcgis/tokens/",
        content: {
          request: "getToken",
          username: "lmdb_user",
          password: "lmdb",
          // clientid may not be necessary; try commented out first, but this is the correct syntax.
          //clientid: "ref.https://lmdb.luc.edu/"  
        },
        handleAs: "text",
        load: tokenObtained,
        error: tokenRequestFailed
      });
    }
```

* If the token is in the response, the tokenObtained function is fired.  This is where all the map layers are queried and added to the map.  Here is a sample of the points of the map being queried:

```
if({{points}}.length != 0){
         var pointFeatureLayerURL = "https://jeez.etl.luc.edu/arcgis/rest/services/campus/lurec_lmdb/FeatureServer/0?token=" + response;

     var queryString = ""
     for( var i=0;  i<{{points}}.length; i++){
         if (queryString == ""){
             queryString += "objectid =" + {{points}}[i];
         }
         else{
             queryString += " OR objectid =" + {{points}}[i];
         }
    
     }


    pointLayer = new FeatureLayer(pointFeatureLayerURL ,{
        mode: FeatureLayer.MODE_SNAPSHOT,
        outFields:["*"]
     });
         pointLayer.setDefinitionExpression(queryString);

```

The `{{points}}` variable is a django list of point ids that are added to a querystring.  This querystring will make a select statement that grabs all points in the `{{points}}` list.

* To add the pointLayer to the actual map, the following is called:

```
map.addLayers([lineLayer,dynamicMapServiceLayer]);
```
The dynamicMapServiceLayer is a layer that displays boundaries and other special areas of LUREC.

* The javascript then renders the map in a div of the html documents with id equal to 'map'.

**_More will be added here when the map code is cleaned up_**

---

