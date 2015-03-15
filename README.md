# RecipeTransformations

## Installation

To install as package while installing dependencies (recommended):

```pip install -r requirements.txt -e .```



Can also install as a package or install dependencies separately: 

```pip install -e .```

```pip install -r requirements.txt```

To run, you’ll need to install maxent_treebank_pos (the trained part of speech tagger) from the NLTK downloader:
```
python
>>> import nltk
>>> nltk.download()
```

To start the Cherrypy webserver:
```python start_webserver.py```


## Database setup

With MongoDB installed, run the following command:
```
mongorestore --db recipes data/recipes
```

The database dump is produced as follows:
```
mongodump  --db recipes --out data
```
