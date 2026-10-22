import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program (1).csv"
df = pd.read_csv(FILE_PATH)
print("File exists:", source.exists())
#checking the dataset
df = pd.read_csv(source)
print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())
print(df.shape)
print(df.columns.tolist())
print("Completely empty rows:", df.isnull().all(axis=1).sum())
print(df.info())
print("Duplicate rows:", df.duplicated().sum())
print(df.tail(10))
print("Total rows:", len(df))
df.isnull().all(axis=1).sum()
df.info()
df.duplicated().sum()
# Display the last 10 rows
print(df.tail(10))
# Count completely empty rows
print("Completely empty rows:", df.isnull().all(axis=1).sum())
#checking the cleaned data set
print(df.shape)
print(df.isnull().sum())
print(df.head())
print(df.tail())
#convert date to datetime format
print(df["Date"] = pd.to_datetime(df["Date"], errors="coerce"))
print(df["Date"].dtype)
print(df["Date"].isna().sum())
print(df["Date"].min())
print(df["Date"].max())
print(df.head())
print(df = df.sort_values("Date").reset_index(drop=True))
print(df["Date"].duplicated().sum())
print(df.duplicated().sum())
print(df.describe())
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()


