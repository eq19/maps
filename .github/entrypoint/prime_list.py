#!/usr/bin/env python

import os
import glob
import talib
import numpy as np
import pandas as pd
import pandas_ta as ta

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras import layers

tf.get_logger().setLevel('ERROR')
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)
os.chdir("/github/workspace/docs/_data/primes")

# use glob to get all the csv files in the folder
# https://www.geeksforgeeks.org/how-to-read-all-csv-files-in-a-folder-in-pandas/

path = os.getcwd()
pd.DataFrame().ta.indicators()
print(talib.get_function_groups())
csv_files = glob.glob(os.path.join(path, "*.csv"))

for f in csv_files:
  # read the csv file
  df_train = pd.read_csv(f, names=["Length", "Diameter", "Height", "Whole weight", "Shucked weight","Viscera weight", "Shell weight", "Age"])

df_train.head()
df_features = df_train.copy()
df_labels = df_features.pop('Age')
df_features = np.array(df_features)
df_features

df_model = tf.keras.Sequential([
  layers.Dense(64),
  layers.Dense(1)
])

df_model.compile(loss = tf.keras.losses.MeanSquaredError(),
  optimizer = tf.keras.optimizers.Adam())
df_model.fit(df_features, df_labels, epochs=10)
