import matplotlib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

METHOD = 1

def run(cursor, subject_id, eeg_file):
    eeg = pd.read_csv(eeg_file)
    print(eeg)
    
    # Indexing/subset selection
    Channels = eeg.iloc[:, 2:]
    Stimulus_Code = eeg.iloc[:, 0]
    Stimulus_Type = eeg.iloc[:, 1]
    
    # OnsetIndices and Labels
    OnsetIndices = []
    count = 0
    labels = []
    for i in range(len(Stimulus_Code)-1):
            if Stimulus_Code[i+1] > 0 and Stimulus_Code[i] == 0:
                OnsetIndices.append(1)
                labels.append(Stimulus_Type[i+1])
            else:
                OnsetIndices.append(0)
                count = count + 1
    
    #print(OnsetIndices)
    OnsetIndices.count(1)
    OnsetIndices.count(0)
    
    # Channel Accuracy
    accuracies =[]
    for j in range(32):
        f = []
        for i in range(len(OnsetIndices)):
            if OnsetIndices[i] == 1:
                f.append(Channels.values[i:i+150, j])
        X_train, X_test, Y_train, Y_test = train_test_split(f, labels, test_size=0.33)
        clf = RandomForestClassifier(n_estimators=100, max_features=40)
        clf.fit(X_train, Y_train)
        accuracies.append(clf.score(X_test, Y_test))
    for i in range(len(accuracies)):
        cursor.execute("insert into scores values(%s, %s, %s, %s)", (subject_id, i+1, METHOD, accuracies[i]))
    #print(accuracies)
