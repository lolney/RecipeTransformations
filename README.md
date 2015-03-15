# RecipeTransformations

## Installation

To install as package while installing dependencies (recommended):

```pip install -r requirements.txt -e .```



Can also install as a package or install dependencies separately: 

```pip install -e .```

```pip install -r requirements.txt```


To start the Cherrypy webserver:
```python start_webserver.py```


## Data setup

With MongoDB installed, run the following command to populate the database:
```
mongorestore --db recipes data/recipes
```

Yyou’ll also need to install maxent_treebank_pos (the trained part of speech tagger) from the NLTK downloader:
```
python
>>> import nltk
>>> nltk.download()
```

For reference, the database dump is produced as follows:
```
mongodump  --db recipes --out data
```
