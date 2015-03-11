# RecipeTransformations

## Installation

To install as package while installing dependencies (recommended):

```pip install -r requirements.txt -e .```



Can also install as a package or install dependencies separately: 

```pip install -e .```

```pip install -r requirements.txt```



To start the Cherrypy webserver:
```python start_webserver.py```


## Database setup

With MongoDB installed, run the following command:
```
mongorestore --db recipes recipes_dump/recipes
```

The database dump is produced as follows:
```
mongodump  --db recipes recipes_dump
```
