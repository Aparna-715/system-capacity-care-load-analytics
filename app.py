
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILE_PATH = BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program (1).csv"

df = pd.read_csv(FILE_PATH)
 
import os
import pandas as pd
from pathlib import Path

# Get the folder where analysis.py is stored
BASE_DIR = Path(__file__).resolve().parent

# Locate the CSV file in the same folder
source = BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program (1).csv"

print("File exists:", source.exists())

# Load the dataset
df = pd.read_csv(source)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

print(df.head())
