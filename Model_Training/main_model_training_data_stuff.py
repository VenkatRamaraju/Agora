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
    training_df = pd.read_csv('overall_training_data.csv', index_col=[0])
    list_of_cols = [x for x in training_df.columns if x in ['Buy', 'Ticker', 'Headlines', 'Conversations']]
    for to_be_added in added_cols:
        list_of_cols.append(to_be_added)

    training_df = training_df[list_of_cols]
    training_df = training_df.dropna()

    new_df = training_df

    training_df['Headlines'] = training_df['Headlines'] * 2
    training_df['Conversations'] = training_df['Conversations'] * 2
    
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

    # filename = 'pickle_model.sav'
    # pickle.dump(LR, open(filename, 'wb'))
    y_prediction = LR.predict(X_test)
    full_prediction = LR.predict(X_total)
    full_acc_score = accuracy_score(y_total, full_prediction)
    print(accuracy_score(y_test, y_prediction))
    print(full_acc_score)
    print()
    loaded_model = pickle.load(open('pickle_model.sav', 'rb'))
    result = loaded_model.score(X_test, y_test)
    print(result)
    print(loaded_model.score(X_total, y_total))


run_model(['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions',
           'shortRatio', 'shortPercentOfFloat'])


"""
# training_df = pd.read_csv('overall_training_data.csv',index_col=[0])
# list_of_cols = [x for x in training_df.columns if x not in ['Buy', 'Ticker', 'Headlines']]

# def subsets(nums):
#         res=[]
#         subset=[]
#         def dfs(i):
#             if i>= len(nums):
#                 res.append(subset.copy())
#                 return
#             subset.append(nums[i])
#             dfs(i+1)
#
#             subset.pop()
#             dfs(i+1)
#         dfs(0)
#         return res
#
# arr = ['payoutRatio', 'beta', 'regularMarketVolume', 'profitMargins', '52WeekChange', 'forwardEps', 'bookValue', 'sharesShort', 'sharesPercentSharesOut', 'trailingEps', 'heldPercentInstitutions', 'heldPercentInsiders', 'mostRecentQuarter', 'nextFiscalYearEnd', 'shortRatio', 'enterpriseValue', 'earningsQuarterlyGrowth', 'sharesShortPriorMonth', 'shortPercentOfFloat', 'pegRatio']
#
# # print(len(arr))
#
# # In[40]:
#
#
# # print(run_model(['earningsQuarterlyGrowth']))
#
#
# # In[41]:
#
#
# max_accuracy = 0
# max_subset_cols = []
# # result = subsets(arr)
#
# # for permutation in result:
# #     permutation_accuracy = run_model(permutation)
# #     if permutation_accuracy > max_accuracy:
# #         max_accuracy = permutation_accuracy
# #         max_subset_cols = permutation.copy()
#
# combs = []
#
# for i in range(1, len(arr)+1):
#     els = [list(x) for x in combinations(arr, i)]
#     combs.extend(els)
#
# max_accuracy = -100000
#
# start_time = time.time()
#
# i = 0
#
# for comb in combs:
#     i += 1
#     acc = run_model(comb)
#     print("Run:", i)
#     print("Accuracy:", acc)
#     print("Columns for model:", comb)
#     print()
#     if acc > max_accuracy:
#         max_accuracy = acc
#         max_subset_cols = comb
#
# print(max_accuracy)
# print(max_subset_cols)
# print("TOTAL TIME:", (time.time() - start_time))

# new_training_df, predictions, new_acc, full_acc = run_model(['beta', 'profitMargins', 'forwardEps', 'bookValue', 'heldPercentInstitutions', 'shortRatio', 'shortPercentOfFloat'], new_training_df)

# new_df = pd.read_csv("../POC/overall_training_data.csv")
new_training_df["agora_preds"] = predictions
new_training_df.to_csv("test_prediction_csv.csv")

# print(new_training_df)
new_training_df['Ticker'] = new_training_df.index
# print(new_training_df)
all_companies = pd.read_csv("../POC/final_db.csv")
all_companies["agora_preds"] = np.nan
all_companies["headline_polarity"] = np.nan
all_companies["conversation_polarity"] = np.nan
print(all_companies.columns)

for index, row in new_training_df.iterrows():
    company_row = all_companies.loc[all_companies["Symbol"] == row["Ticker"]]
    all_companies["agora_preds"][company_row.index.item()] = row["agora_preds"]
    all_companies["headline_polarity"][company_row.index.item()] = row["Headlines"]
    all_companies["conversation_polarity"][company_row.index.item()] = row["Conversations"]
    # print(company_row.index.item())
    # all_companies[""]

# print(all_companies)
all_companies.to_csv("all_companies_w_preds.csv")
# print(new_acc)
# print(full_acc)
# print(len(predictions))
# print(predictions)
"""
