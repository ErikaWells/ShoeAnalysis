import streamlit as st
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df['Release.Date'] = pd.to_datetime(df['Release.Date'], errors='coerce')
    df['daysfrommarch'] = (df['Release.Date'] - pd.to_datetime("2025-03-31")).dt.days
    df = df.dropna(subset=['rank', 'price', 'daysfrommarch', 'Main.Color'])
    return df

df = load_data()

st.title("GOAT Ranking Regression Analysis")

# Select independent variables
cols_to_include = st.multiselect(
    "Choose predictors to include:",
    ['price', 'daysfrommarch', 'Designer', 'Main.Color', 'Technology', 'Category'],
    default=['price', 'daysfrommarch', 'Designer', 'Main.Color', 'Technology', 'Category']
)

# Build and fit model
if cols_to_include:
    X = pd.get_dummies(df[cols_to_include], drop_first=True)
    y = df['rank']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    st.subheader("Model Summary")
    st.text(model.summary())

    st.subheader("Visualize Effect of Color")
    if 'Main.Color' in cols_to_include:
        color_effects = model.params.filter(like='Main.Color')
        color_se = model.bse.filter(like='Main.Color')
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=color_effects.index.str.replace('Main.Color', ''), y=color_effects.values, yerr=color_se.values, ax=ax)
        plt.xticks(rotation=45)
        plt.title("Effect of Main Color on Rank")
        plt.ylabel("Coefficient Estimate")
        st.pyplot(fig)
