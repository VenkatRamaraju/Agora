#!/usr/bin/env python
# coding: utf-8

"""
Authors: Venkat Ramaraju, Jayanth Rao
Functionality implemented:
- Prepares data for model training
"""

# Imports and dependencies
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import accuracy_score
from itertools import combinations
import time
import pickle

# Global data
new_training_df = pd.DataFrame()


def run_model(added_cols):
    """
    Runs the pickled logistic regression machine learning model on the subset of columns provided. The subset of
    columns have been feature selected to derive the highest accuracy.
    :param added_cols: set of columns that will be used to train the machine learning model.
    """
    training_df = pd.read_csv('final_dataset.csv', index_col=[0])
    list_of_cols = [x for x in training_df.columns if x in ['Buy', 'Ticker', 'headline_polarity', 'convo_polarity']]
    for to_be_added in added_cols:
        list_of_cols.append(to_be_added)

    training_df = training_df[list_of_cols]
    training_df = training_df.dropna()

    training_df['headline_polarity'] = training_df['headline_polarity'] * 2
    training_df['convo_polarity'] = training_df['convo_polarity'] * 2
    
    # Creating training and testing datasets
    X_total = training_df[[x for x in training_df.columns if x not in ['Buy', 'Ticker']]]
    y_total = training_df['Buy']
    X_train, X_test, y_train, y_test = train_test_split(X_total, y_total, test_size=0.33, random_state=42)
    
    # Logistic Regression Mode
    LR = LogisticRegression(class_weight='balanced', solver='lbfgs', max_iter=1000)
    try:
        LR = LR.fit(X_train, y_train)
    except Exception as e:
        return -1

    filename = 'pickle_model.sav'
    pickle.dump(LR, open(filename, 'wb'))
    y_prediction = LR.predict(X_test)
    full_prediction = LR.predict(X_total)
    full_acc_score = accuracy_score(y_total, full_prediction)

    loaded_model = pickle.load(open('pickle_model.sav', 'rb'))
    result = loaded_model.score(X_test, y_test)

def main():
    run_model(['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions',
               'shortRatio', 'shortPercentOfFloat'])

if __name__ == "__main__":
    main()