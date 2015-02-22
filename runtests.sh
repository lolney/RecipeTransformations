#!/bin/bash

pip install --upgrade -r requirements.txt -e .
py.test test/parsing.py test/findposteriors.py