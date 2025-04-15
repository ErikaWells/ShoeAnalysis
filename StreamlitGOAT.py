import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_dataset.csv")
    except FileNotFoundError:
        st.error("The file 'cleaned_dataset.csv' was not found. Please upload it.")
        return pd.DataFrame()
    
    df['Release.Date'] = pd.to_datetime(df['Release.Date'], errors='coerce')
    df['daysfrommarch'] = (df['Release.Date'] - pd.to_datetime("2025-03-31")).dt.days
    return df.dropna(subset=['rank', 'price', 'daysfrommarch'])

df = load_data()

st.title("Explore Shoe Dataset with Histograms")

if not df.empty:
    column = st.selectbox(
        "Choose a column to visualize:",
        ['price', 'rank', 'daysfrommarch', 'Designer', 'Main.Color', 'Technology', 'Category']
    )

    st.subheader(f"Histogram of {column}")

    fig, ax = plt.subplots(figsize=(8, 5))
    
    if df[column].dtype == 'object':
        sns.countplot(data=df, x=column, ax=ax, order=df[column].value_counts().index)
        ax.set_ylabel("Count")
    else:
        sns.histplot(df[column], bins=20, kde=True, ax=ax)
        ax.set_ylabel("Frequency")
    
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("No data loaded. Please check your CSV file.")

