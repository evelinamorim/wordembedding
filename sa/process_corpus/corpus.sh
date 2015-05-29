#!/bin/bash

# prepare training and test corpus

# shuflle the corpus
# python3 shuffle.py

# take the first 208921 lines for training (80% of total reviews)
# head -208921 shuffle_drugs_reviews.json >> train_drugs_reviews.json

#take the last 52231 lines for testing (20% of total reviews)
# tail -52231 shuffle_drugs_reviews.json >> test_drugs_reviews.json

#fix the json given for a format that json python library understands (training)
python3 process_json.py -f train_drugs_reviews.json 208921
mv new_train_drugs_reviews.json train_drugs_reviews.json

#fix the json given for a format that json python library understands (testing)
python3 process_json.py -f test_drugs_reviews.json 52231
mv new_test_drugs_reviews.json test_drugs_reviews.json

#get only the review text from json in order to train word2 vec
python3 process_json.py -r train_drugs_reviews.json
