
import pandas as pd
from pathlib import Path

# Get the folder where this Python file is saved
BASE_DIR = Path(__file__).resolve().parent

# Find the HHS dataset
FILE_PATH = BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program (1).csv"

# Load the dataset
df = pd.read_csv(FILE_PATH)

# Display the first five rows
print("First five rows:")
print(df.head())

# Display dataset dimensions
print("\nDataset shape:")
print(df.shape)

# Display column names
print("\nColumn names:")
print(df.columns.tolist())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())
