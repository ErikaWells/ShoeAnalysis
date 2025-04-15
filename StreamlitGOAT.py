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
    df = df.dropna(subset=['price', 'daysfrommarch', 'MainColor'])
    return df

df = load_data()

st.title("GOAT Shoe Data Explorer")

# Define color options
color_palette = {
    "Default (blue)": "deep",
    "Vibrant (colorful)": "bright",
    "Muted (earth tones)": "muted",
    "Dark Mode": "dark",
    "Custom Red": ["#e74c3c"]
}

# Drop unwanted columns
columns_to_use = [col for col in df.columns if col not in ['rank', 'SKU', 'Nickname']]

tab1, tab2 = st.tabs(["📊 Histograms", "📈 Compare Two Variables"])

# --------------------- TAB 1: HISTOGRAMS ---------------------
with tab1:
    st.subheader("Explore One Variable")

    # Optional filters
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox("Filter by Category", ["All"] + sorted(df["Category"].dropna().unique()))
    with col2:
        selected_designer = st.selectbox("Filter by Designer", ["All"] + sorted(df["Designer"].dropna().unique()))

    # Apply filters
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    if selected_designer != "All":
        filtered_df = filtered_df[filtered_df["Designer"] == selected_designer]

    # Select variable
    column_to_plot = st.selectbox(
        "Select a variable to see its distribution:",
        [col for col in columns_to_use if col not in ['ReleaseDate']]
    )

    # Choose color scheme
    selected_palette = st.selectbox("Choose color scheme:", list(color_palette.keys()))
    sns.set_palette(color_palette[selected_palette])

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    if pd.api.types.is_numeric_dtype(filtered_df[column_to_plot]):
        sns.histplot(filtered_df[column_to_plot].dropna(), bins=30, kde=True, ax=ax)
    else:
        sns.countplot(x=filtered_df[column_to_plot], order=filtered_df[column_to_plot].value_counts().index, ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title(f"Distribution of {column_to_plot}")
    st.pyplot(fig)

# --------------------- TAB 2: COMPARISONS ---------------------
with tab2:
    st.subheader("Compare Two Variables")

    x_var = st.selectbox("Select X-axis variable", columns_to_use)
    y_var = st.selectbox("Select Y-axis variable", columns_to_use)

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # Pick chart type depending on data types
    if pd.api.types.is_numeric_dtype(df[x_var]) and pd.api.types.is_numeric_dtype(df[y_var]):
        sns.scatterplot(x=df[x_var], y=df[y_var], ax=ax2)
    elif pd.api.types.is_categorical_dtype(df[x_var]) or df[x_var].dtype == "object":
        sns.boxplot(x=df[x_var], y=df[y_var], ax=ax2)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    else:
        sns.violinplot(x=df[x_var], y=df[y_var], ax=ax2)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

    ax2.set_title(f"{y_var} vs {x_var}")
    st.pyplot(fig2)


