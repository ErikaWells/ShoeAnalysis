import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df['ReleaseDate'] = pd.to_datetime(df['ReleaseDate'], errors='coerce')
    df['daysfrommarch'] = (df['ReleaseDate'] - pd.to_datetime("2025-03-31")).dt.days
    df = df.dropna(subset=['rank', 'price', 'daysfrommarch', 'MainColor'])
    return df

df = load_data()

st.title("GOAT Shoe Data Explorer")

# Dropdown to pick a column to visualize
column_to_plot = st.selectbox(
    "Select a variable to see its distribution:",
    ['price', 'rank', 'daysfrommarch', 'Designer', 'MainColor', 'Technology', 'Category']
)

# Plotting
st.subheader(f"Histogram of {column_to_plot}")

fig, ax = plt.subplots(figsize=(10, 5))

if pd.api.types.is_numeric_dtype(df[column_to_plot]):
    sns.histplot(df[column_to_plot].dropna(), bins=30, kde=True, ax=ax)
else:
    # Countplot for categorical variables
    sns.countplot(x=df[column_to_plot], order=df[column_to_plot].value_counts().index, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

st.pyplot(fig)

