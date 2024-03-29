# -*- coding: utf-8 -*-
"""Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QlQko4aKAOpU8iDkJVLH6s_Cw68hjTMV
"""

!pip install imblearn

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from imblearn.over_sampling import SMOTE

df  = pd.read_csv('/content/cuisines.csv')



#Check datashape
df.head()

#datainfo
df.info()

#plot data as bars by calling barh()
df.cuisine.value_counts().plot.barh()

#how much data is available per cuisine
thai_df = df[(df.cuisine == "thai")]
japanese_df = df[(df.cuisine == "japanese")]
chinese_df = df[(df.cuisine == "chinese")]
indian_df = df[(df.cuisine == "indian")]
korean_df = df[(df.cuisine == "korean")]

#it will print number of rows and columns of each cuisine
print(f'thai df: {thai_df.shape}')
print(f'japanese df: {japanese_df.shape}')
print(f'chinese df: {chinese_df.shape}')
print(f'indian df: {indian_df.shape}')
print(f'korean df: {korean_df.shape}')



"""**Discovering** **ingredients**

> Now you can dig deeper into the data and learn what are the typical ingredients per cuisine. You should clean out recurrent data that creates confusion between cuisines, so let's learn about this problem.

Create a function **create_ingredient()** in Python to create an ingredient dataframe. This function will start by dropping an unhelpful column and sort through ingredients by their count:


"""

def create_ingredient_df(df):
    ingredient_df = df.T.drop(['cuisine','Unnamed: 0']).sum(axis=1).to_frame('value')
    ingredient_df = ingredient_df[(ingredient_df.T != 0).any()]
    ingredient_df = ingredient_df.sort_values(by='value', ascending=False,
    inplace=False)
    return ingredient_df
    df.head()

"""2. Call create_ingredient() and plot it calling barh():"""

thai_ingredient_df = create_ingredient_df(thai_df)
thai_ingredient_df.head(10).plot.barh()

indian_ingredient_df = create_ingredient_df(indian_df)
indian_ingredient_df.head(10).plot.barh()

"""Now, drop the most common ingredients that create confusion between distinct cuisines, by calling drop():

Everyone loves rice
, garlic and ginger!
"""

feature_df= df.drop(['cuisine','Unnamed: 0','rice','garlic','ginger'], axis=1)
labels_df = df.cuisine #.unique()
feature_df.head()

"""**Balance the dataset**

Now that you have cleaned the data, use SMOTE - "Synthetic Minority Over-sampling Technique" - to balance it.

Call fit_resample(), this strategy generates new samples by interpolation.
"""

oversample = SMOTE()
transformed_feature_df, transformed_label_df = oversample.fit_resample(feature_df, labels_df)

"""By balancing your data, you'll have better results when classifying it. Think about a binary classification. If most of your data is one class, a ML model is going to predict that class more frequently, just because there is more data for it. Balancing the data takes any skewed data and helps remove this imbalance.

2. Now you can check the numbers of labels per ingredient:
"""

print(f'new label count: {transformed_label_df.value_counts()}')
print(f'old label count: {df.cuisine.value_counts()}')

"""The data is nice and clean, balanced, and very delicious!

The last step is to save your balanced data, including labels and features, into a new dataframe that can be exported into a file:
"""

transformed_df = pd.concat([transformed_label_df,transformed_feature_df],axis=1, join='outer')

transformed_df.head()
transformed_df.info()
transformed_df.to_csv("/content/cleaned_cuisines.csv")