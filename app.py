import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Approval Dashboard", layout="wide")

st.title("🏦 Loan Approval Analysis & Interactive Dashboard")
st.markdown("Final Year Project - Data Analytics")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("LP_Train.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("🔎 Filter Data")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].dropna().unique(),
    default=df["Gender"].dropna().unique()
)

property_filter = st.sidebar.multiselect(
    "Select Property Area",
    options=df["Property_Area"].dropna().unique(),
    default=df["Property_Area"].dropna().unique()
)

filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Property_Area"].isin(property_filter))
]

# KPI Metrics
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

total_apps = len(filtered_df)
approved = len(filtered_df[filtered_df["Loan_Status"] == "Y"])
approval_rate = round((approved / total_apps) * 100, 2) if total_apps > 0 else 0

col1.metric("Total Applications", total_apps)
col2.metric("Approved Loans", approved)
col3.metric("Approval Rate (%)", approval_rate)

st.markdown("---")

# Visualization Section
col4, col5 = st.columns(2)

with col4:
    st.subheader("Loan Status Distribution")
    fig1, ax1 = plt.subplots()
    sns.countplot(x="Loan_Status", data=filtered_df, ax=ax1)
    st.pyplot(fig1)

with col5:
    st.subheader("Credit History Impact")
    fig2, ax2 = plt.subplots()
    sns.countplot(x="Credit_History", hue="Loan_Status", data=filtered_df, ax=ax2)
    st.pyplot(fig2)

st.markdown("---")

# Income Analysis
st.subheader("💰 Income Analysis")

fig3, ax3 = plt.subplots()
sns.boxplot(x="Loan_Status", y="ApplicantIncome", data=filtered_df, ax=ax3)
st.pyplot(fig3)

st.markdown("---")

# Correlation Heatmap
st.subheader("📈 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(include=np.number)

if not numeric_df.empty:
    fig4, ax4 = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax4)
    st.pyplot(fig4)
else:
    st.warning("Not enough numeric data for correlation.")

st.markdown("---")

# Loan Prediction Demo (Rule-Based Logic)
st.subheader("🔮 Loan Approval Prediction (Demo Model)")

income = st.number_input("Applicant Income", min_value=0)
credit = st.selectbox("Credit History (1 = Good, 0 = Bad)", [1, 0])
loan_amount = st.number_input("Loan Amount", min_value=0)

if st.button("Predict Loan Status"):
    if credit == 1 and income > 3000 and loan_amount < 200:
        st.success("Loan Likely to be Approved ✅")
    else:
        st.error("Loan Likely to be Rejected ❌")

st.markdown("---")

st.success("✅ Interactive Dashboard Loaded Successfully")
