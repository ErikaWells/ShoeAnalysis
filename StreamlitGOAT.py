import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df['ReleaseDate'] = pd.to_datetime(df['ReleaseDate'], errors='coerce')
    df['daysfrommarch'] = (df['ReleaseDate'] - pd.to_datetime("2025-03-31")).dt.days
    df = df.dropna(subset=['price', 'daysfrommarch', 'MainColor'])
    return df

df = load_data()

st.title("Top Shoes This March")

# Drop columns
columns_to_use = [col for col in df.columns if col not in ['rank', 'SKU', 'Nickname', 'shoe', 'Colorway', 'ReleaseDate']]


tab1, tab2, tab3 = st.tabs(["📊 Histograms", "📈 Compare Two Variables", "🏆 KPI Dashboard"])

# --------------------- TAB 1: HISTOGRAMS ---------------------
with tab1:
    st.subheader("Explore One Variable")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_maincolor = st.selectbox("Filter by Main Color", ["All"] + sorted(df["MainColor"].dropna().unique()))
    with col2:
        selected_category = st.selectbox("Filter by Category", ["All"] + sorted(df["Category"].dropna().unique()))
    with col3:
        selected_designer = st.selectbox("Filter by Designer", ["All"] + sorted(df["Designer"].dropna().unique()))

    # Apply filters
    filtered_df = df.copy()
    if selected_maincolor != "All":
        filtered_df = filtered_df[filtered_df["MainColor"] == selected_maincolor]
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    if selected_designer != "All":
        filtered_df = filtered_df[filtered_df["Designer"] == selected_designer]

    # Select column to plot
    column_to_plot = st.selectbox(
        "Select a variable to see its distribution:",
        columns_to_use
    )

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

# --------------------- TAB 3: KPI DASHBOARD ---------------------
with tab3:
    st.subheader("🏆 KPI Summary")

    # Select Top N Shoes
    top_n = st.selectbox("Choose # of Top Shoes", [10, 20, 50, 100, 182], index=0)

    # Create a fun, colorful column layout for KPI Cards
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    # Filter Data based on top N
    top_shoes_df = df.head(top_n)

    # Metric 1: Most Expensive Shoe by Rank
    most_expensive_shoe = top_shoes_df.loc[top_shoes_df['price'].idxmax()]
    most_expensive_price = most_expensive_shoe['price']
    most_expensive_name = most_expensive_shoe['shoe']
    most_expensive_designer = most_expensive_shoe['Designer']
    most_expensive_color = most_expensive_shoe['MainColor']
    most_expenssive_link = most_expensive_shoe['productlink']

    # Metric 2: Avg Price of Top N Shoes
    avg_price_top = top_shoes_df['price'].mean()

    # Metric 3: Avg Rank of Top N Shoes
    avg_rank_top = top_shoes_df['rank'].mean()

    # KPI card 1 
    with kpi_col1:
        st.markdown(f"""
            <div style='background-color:#FF6F61; padding:10px; border-radius:8px; text-align:center;'>
                <h2 style='color:white; margin-bottom:10px;'>Most Expensive Shoe</h2>
                <p style='color:white; font-size:18px; margin:0;'><b>{most_expensive_name}</b></p>
                <p style='color:white; font-size:16px; margin:0;'>${most_expensive_price} by {most_expensive_designer} ({most_expensive_color})</p>
                <a href='{most_expensive_shoe['productlink']}' target='_blank' style='color:white; text-decoration:underline;'>View on GOAT</a>
            </div>
        """, unsafe_allow_html=True)

    # KPI Card 2 - Average Price of Top N Shoes
    with kpi_col2:
        st.markdown(f"""
            <div style='background-color:#56B4D3; padding:10px; border-radius:8px; text-align:center;'>
                <h2 style='color:white; margin-bottom:10px;'>Average Price of Top {top_n} Shoes</h2>
                <p style='color:white; font-size:22px;'>${avg_price_top:.2f}</p>
            </div>
        """, unsafe_allow_html=True)

    # KPI Card 3 - Most Popular Color of Top N Shoes
    most_popular_color = top_shoes_df['MainColor'].mode()[0]
    
    with kpi_col3:
        st.markdown(f"""
            <div style='background-color:#D9BF77; padding:10px; border-radius:8px; text-align:center;'>
                <h2 style='color:white; margin-bottom:10px;'>Most Popular Color in Top {top_n} Shoes</h2>
                <p style='color:white; font-size:22px;'>{most_popular_color}</p>
            </div>
        """, unsafe_allow_html=True)# KPI Card 1 - Most Expensive Shoe


    # Section 2: List Top N Shoes with Details
    st.subheader(f"🔥 Top {top_n} Shoes")

    # Create a table to show shoe details
    top_shoes_df = top_shoes_df[['rank', 'shoe', 'price', 'Designer', 'MainColor', 'SKU', 'productlink']]

    # Show top N shoes with links
    for index, row in top_shoes_df.iterrows():
        st.markdown(f"<div style='background-color:#F1F3F4; border-radius:8px; padding:10px; margin-bottom:10px;'>"
                    f"<h4>{row['rank']}. {row['shoe']}</h4>"
                    f"<p><b>Price:</b> ${row['price']:.2f} | <b>Designer:</b> {row['Designer']} | <b>Color:</b> {row['MainColor']}</p>"
                    f"<a href='{row['productlink']}' target='_blank'>View on GOAT</a>"
                    f"</div>", unsafe_allow_html=True)


