# RecipeTransformations

## Installation

Clone the repository and name the project directory 'Recipes':

```git clone https://github.com/lolney/RecipeTransformations.git Recipes```

To install as package while installing dependencies (recommended):

```pip install -r requirements.txt -e .```



Can also install as a package or install dependencies separately: 

```pip install -e .```

```pip install -r requirements.txt```


## Data setup

With MongoDB installed, run the following command to populate the database:
```
mongorestore --db recipes data/recipes
```

You’ll also need to install maxent_treebank_pos (the trained part of speech tagger) from the NLTK downloader:
```
python
>>> import nltk
>>> nltk.download()
```

For reference, the database dump is produced as follows:
```
mongodump  --db recipes --out data
```

## Running

The program interface, which takes an AllRecipes url as input and returns the parsed representation of the recipe, can be run as follows: 
```
python
>>> from recipetransform.nlp.parsing import parserProgramInterface
>>> url = "allrecipes.com/Recipe/Asian-Beef-with-Snow-Peas"
>>> parserProgramInterface(url)
```

The autograder is already present in the top-level directory and configured properly. To run, make sure the project directory is called 'Recipes', then set the working directory to ../Recipes/ and run this command:
```python autograder.py```

To access the web interface, start the Cherrypy webserver as follows and navigate to 127.0.0.1:8080:
```python start_webserver.py```
