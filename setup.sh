#!/bin/bash
pip3 install -r production_requirements.txt
python3 setup.py
python3 -m spacy download ru_core_news_sm