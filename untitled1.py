#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 00:43:53 2021

@author: eshankeluskar
"""

from urllib.request import urlopen
import streamlit as st
import pandas as pd
import numpy as np
#import shap
import xgboost
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

st.write("""
# IPL Player Value Prediction App
This app predicts the **player value** in IPL!""")

st.sidebar.header('User Input Features')


# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    input_df = input_df.drop(['Rank','Player','Team'], axis=1)
    input_df['Salary'] = input_df['Salary'].str.replace(',', '').str.replace('$', '').astype(float)
    input_df = input_df.fillna('0')
else:
    def user_input_features():
        RAA = st.sidebar.slider('RAA', -292.00, 410.00, -21.00)
        Wins = st.sidebar.slider('Wins', -0.98, 1.41, -0.07)
        EFscore = st.sidebar.slider('EFscore', 0.00, 0.24, 0.04)
        Salary = st.sidebar.slider('Salary', 15000.00, 2656250.00, 581584.48)
        data = {'RAA': RAA,
                'Wins': Wins,
                'EFscore': EFscore,
                'Salary': Salary
                }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()


# Displays the user input features
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(input_df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using sidebar input parameters (shown below).')
    st.write(input_df)

train_df = pd.read_csv('/Users/eshankeluskar/Documents/Mahe/sem 3/minorproject2/IPL-player-value-prediction-main/data/full-data.csv')
values = {'Salary': 0}
train_df = train_df.fillna(value=values)

X = train_df[['RAA', 'Wins', 'EFscore', 'Salary']]
y = train_df[['Value']]

xgb_model = XGBRegressor().fit(X, y)

# Apply model to make predictions
prediction = xgb_model.predict(input_df)

st.header('Prediction of Value (in currency)')
st.write(prediction)
st.write('---')
