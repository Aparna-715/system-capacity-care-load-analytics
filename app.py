# ============================================================
# SYSTEM CAPACITY & CARE LOAD ANALYTICS
# Unaccompanied Children Program
# ============================================================

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ============================================================
# 1. STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="System Capacity & Care Load Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("System Capacity & Care Load Analytics")
st.subheader("Unaccompanied Children Program")

st.write(
    "This application explores aggregate data on children in "
    "CBP custody and HHS care."
)


# ============================================================
# 2. LOAD DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FILE_PATH = (
    BASE_DIR / "HHS_Unaccompanied_Alien_Children_Program (1).csv"
)

if not FILE_PATH.exists():
    st.error(f"CSV file not found: {FILE_PATH.name}")
    st.info(
        "Place the CSV file in the same folder as app.py, "
        "and check that its filename matches exactly."
    )
    st.stop()

try:
    df = pd.read_csv(FILE_PATH)
except Exception as error:
    st.error(f"Unable to read the CSV file: {error}")
    st.stop()

st.success("Dataset loaded successfully!")


# ============================================================
# 3. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Date",
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error("Some required columns are missing:")
    st.write(missing_columns)
    st.stop()


# ============================================================
# 4. ORIGINAL DATASET INSPECTION
# ============================================================

st.header("1. Dataset Inspection")

col1, col2 = st.columns(2)

with col1:
    st.metric("Original Rows", len(df))

with col2:
    st.metric("Original Columns", len(df.columns))

st.write("### Column Names")
st.write(df.columns.tolist())

st.write("### First Five Rows")
st.dataframe(df.head(), use_container_width=True)

st.write("### Last Ten Rows")
st.dataframe(df.tail(10), use_container_width=True)

st.write("### Original Missing Values")
st.dataframe(
    df.isnull().sum().rename("Missing Values")
)

st.write(
    "Completely empty rows:",
    int(df.isnull().all(axis=1).sum())
)

st.write(
    "Exact duplicate rows:",
    int(df.duplicated().sum())
)

st.write("### Original Data Types")
st.dataframe(
    df.dtypes.astype(str).rename("Data Type")
)


# ============================================================
# 5. CLEAN DATA
# ============================================================

st.header("2. Data Cleaning")

# Remove rows where every column is missing.
df = df.dropna(how="all").copy()

# Convert Date to datetime.
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

# Convert measurement columns to numeric values.
numeric_columns = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column]
        .astype("string")
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

# Sort chronologically, with missing dates at the end.
df = df.sort_values(
    "Date",
    na_position="last"
).reset_index(drop=True)

st.write("### Cleaning Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows After Cleaning", len(df))

with col2:
    st.metric("Columns", len(df.columns))

st.write("### Missing Values After Conversion")
st.dataframe(
    df.isnull().sum().rename("Missing Values")
)

st.write("### Cleaned Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

st.write("### Cleaned Dataset: Last Ten Rows")
st.dataframe(df.tail(10), use_container_width=True)


# ============================================================
# 6. DATA VALIDATION
# ============================================================

st.header("3. Data Validation")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Missing Dates",
        int(df["Date"].isna().sum())
    )

with col2:
    st.metric(
        "Duplicate Dates",
        int(df["Date"].duplicated().sum())
    )

with col3:
    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

valid_dates = df["Date"].dropna()

if not valid_dates.empty:
    st.write("Earliest Date:", valid_dates.min().date())
    st.write("Latest Date:", valid_dates.max().date())

st.write("### Summary Statistics")
st.dataframe(df[numeric_columns].describe(), use_container_width=True)


# ============================================================
# 7. CHART 1: CHILDREN IN HHS CARE OVER TIME
# ============================================================

st.header("4. Children in HHS Care Over Time")

hhs_chart_df = df.dropna(
    subset=["Date", "Children in HHS Care"]
)

if hhs_chart_df.empty:
    st.warning("There is no valid data available for this chart.")
else:
    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(
        hhs_chart_df["Date"],
        hhs_chart_df["Children in HHS Care"],
        label="Children in HHS Care"
    )

    ax.set_title("Children in HHS Care Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Children")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# 8. CHART 2: CBP CUSTODY VS HHS CARE
# ============================================================

st.header("5. CBP Custody vs HHS Care Over Time")

comparison_df = df.dropna(
    subset=[
        "Date",
        "Children in CBP custody",
        "Children in HHS Care"
    ]
)

if comparison_df.empty:
    st.warning("There is no valid data available for this chart.")
else:
    fig, ax = plt.subplots(figsize=(14, 5))

    ax.plot(
        comparison_df["Date"],
        comparison_df["Children in CBP custody"],
        label="Children in CBP Custody"
    )

    ax.plot(
        comparison_df["Date"],
        comparison_df["Children in HHS Care"],
        label="Children in HHS Care"
    )

    ax.set_title("CBP Custody vs HHS Care Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Children")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# 9. FINAL DATASET VIEW
# ============================================================

st.header("6. View Complete Dataset")

if st.checkbox("Show the complete cleaned dataset"):
    st.dataframe(df, use_container_width=True)

st.caption(
    "These are analytical indicators based on aggregate data. "
    "They are not official measures of system-wide backlog."
)

st.success("Dataset inspection and exploratory analysis completed!")
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    df["Date"],
    df["Children in CBP custody"],
    label="Children in CBP Custody"
)

ax.plot(
    df["Date"],
    df["Children in HHS Care"],
    label="Children in HHS Care"
)

ax.set_title("CBP Custody vs HHS Care Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Children")
plt.xticks(rotation=45)

ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()

st.pyplot(fig)
plt.close(fig)
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    df["Date"],
    df["Children apprehended and placed in CBP custody*"],
    label="Apprehensions"
)

ax.plot(
    df["Date"],
    df["Children transferred out of CBP custody"],
    label="Transfers out of CBP"
)

ax.plot(
    df["Date"],
    df["Children discharged from HHS Care"],
    label="HHS Discharges"
)

ax.set_title("Apprehensions, Transfers, and Discharges Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Children")

plt.xticks(rotation=45)
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

movement_cols = [
    "Children apprehended and placed in CBP custody*",
    "Children transferred out of CBP custody",
    "Children discharged from HHS Care"
]

st.subheader("Summary Statistics: Child Movement")

movement_summary = df[movement_cols].describe().round(2)

st.dataframe(movement_summary, use_container_width=True)
#Calculate KPI 1 — Net Intake Pressure
# Define the required columns
apprehensions = "Children apprehended and placed in CBP custody*"
discharges = "Children discharged from HHS Care"

# Calculate Net Intake Pressure
df["Net Intake Pressure"] = df[apprehensions] - df[discharges]

# Display the first 10 rows
st.subheader("Net Intake Pressure Analysis")

st.dataframe(
    df[["Date", apprehensions, discharges, "Net Intake Pressure"]].head(10),
    use_container_width=True
)

# Plot the trend
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    df["Date"],
    df["Net Intake Pressure"],
    label="Net Intake Pressure"
)

ax.axhline(0, linestyle="--", alpha=0.7)
ax.set_title("Daily Net Intake Pressure Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Apprehensions - HHS Discharges")

plt.xticks(rotation=45)
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Calculate summary values
average_pressure = round(df["Net Intake Pressure"].mean(), 2)
maximum_pressure = df["Net Intake Pressure"].max()

# Display KPI metrics
col1, col2 = st.columns(2)

col1.metric("Average Net Intake Pressure", f"{average_pressure:,.2f}")
col2.metric("Maximum Net Intake Pressure", f"{maximum_pressure:,.2f}")
# Count positive, negative, and zero values
positive_days = (df["Net Intake Pressure"] > 0).sum()
negative_days = (df["Net Intake Pressure"] < 0).sum()
zero_days = (df["Net Intake Pressure"] == 0).sum()

# Display results in the dashboard
st.subheader("Net Intake Pressure Breakdown")

col1, col2, col3 = st.columns(3)

col1.metric("Positive Values", f"{positive_days:,}")
col2.metric("Negative Values", f"{negative_days:,}")
col3.metric("Zero Values", f"{zero_days:,}")
#KPI 2: Care Load Volatility Index
# Convert HHS Care column to numeric
df["Children in HHS Care"] = pd.to_numeric(
    df["Children in HHS Care"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip(),
    errors="coerce"
)

st.success("HHS Care column converted to numeric!")

st.write("Column data type:", str(df["Children in HHS Care"].dtype))
st.write("Missing values:", int(df["Children in HHS Care"].isna().sum()))

# Sort data chronologically before calculating changes
df = df.sort_values("Date").reset_index(drop=True)

# Calculate change in HHS Care
df["HHS Care Change"] = df["Children in HHS Care"].diff()

# Display first 10 rows
st.subheader("HHS Care Change: First 10 Rows")

st.dataframe(
    df[["Date", "Children in HHS Care", "HHS Care Change"]].head(10),
    use_container_width=True
)

# Calculate Care Load Volatility
care_volatility = df["HHS Care Change"].std()

st.metric(
    "KPI 2 – Care Load Volatility",
    f"{care_volatility:,.2f}" if pd.notna(care_volatility) else "N/A"
)

# Plot changes over time
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(
    df["Date"],
    df["HHS Care Change"],
    label="Change in HHS Care"
)

ax.axhline(0, linestyle="--", alpha=0.7)
ax.set_title("KPI 2: Care Load Volatility Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Change in Number of Children")

plt.xticks(rotation=45)
ax.legend()
ax.grid(True, alpha=0.3)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)