from flask import Flask, render_template, request
import tensorflow as tf
import pandas as pd
import numpy as np
import logging
import joblib
import json
import sys
import os

from spacy.lang.en import English
from sklearn.preprocessing import LabelEncoder

# Current directory
current_dir = os.path.dirname(__file__)

app = Flask(__name__, static_folder='static', template_folder='template')

# Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def predict():
    return render_template('prediction.html')

@app.route('/script.js')
def script():
    return app.send_static_file('script.js')

# Make function to split sentences into characters
def split_chars(text):
    return " ".join(list(text))

# Create a function to read the lines of a document
def get_lines(filename):
    """
    Reads filename (a text filename) and returns the lines of text as a list.

    Args:
        filename: a string containing the target filepath.

    Returns:
        A list of strings with one string per line from the target filename.
    """

    with open(filename, "r") as file:
        return file.readlines()

def preprocess_text_with_line_numbers(filename):
    """
    Returns a list of dictionaries of abstract line data.

    Args:
        filename: Reads it's contents and sorts through each line,
                  extracting things like target label, the text of the sentence,
                  how many sentences are in the current abstract and what sentence
                  number the target line is.

    """
    input_lines = get_lines(filename)   # get all lines from filename
    abstract_lines = ""                 # create an empty abstract
    abstract_samples = []               # create an empty list of abstracts

    # Loop through each line in the target file
    for line in input_lines:
        if line.startswith("###"):  # check to see if the line is an ID line
            abstract_id = line
            abstract_lines = ""     # reset the abstract string if the line is an ID line
        elif line.isspace():        # check to see if line is a new line
            abstract_line_split = abstract_lines.splitlines()   # split abstract into separate lines

            # Iterate through each line in a single abstract and count them at the same time
            for abstract_line_number, abstract_line in enumerate(abstract_line_split):
                line_data = {}                                          # create an empty dictionary for each line
                target_text_split = abstract_line.split("\t")           # split target label from text
                line_data["target"] = target_text_split[0]              # get the target label from text
                line_data["text"] = target_text_split[1].lower()        # get target text and lower it
                line_data["line_number"] = abstract_line_number         # what number line does the line appear in the abstract
                line_data["total_lines"] = len(abstract_line_split) - 1 # how many total lines are there in the target abstract? (start from 0)
                abstract_samples.append(line_data)                      # add line data to abstract samples list

        else:   # if the above conditions aren't fulfilled, the line contains a labelled sentence
            abstract_lines += line

    return abstract_samples

# text = "This RCT examined the efficacy of a manualized social intervention for children with HFASDs. Participants were randomly assigned to treatment or wait-list conditions. Treatment included instruction and therapeutic activities targeting social skills, face-emotion recognition, 
if __name__ == '__main__':
    app.run(debug=True)
