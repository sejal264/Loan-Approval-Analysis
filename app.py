import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Loan Approval Analysis")

# Load dataset
df = pd.read_csv("LP_Train.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Sidebar
st.sidebar.title("Select Analysis")
option = st.sidebar.selectbox(
    "Choose option",
    ["Loan Status", "Income Analysis", "Credit History", "Property Area"]
)

# Loan Status
if option == "Loan Status":
    st.subheader("Loan Approval Status")
    fig, ax = plt.subplots()
    sns.countplot(x="Loan_Status", data=df, ax=ax)
    st.pyplot(fig)

# Income Analysis
elif option == "Income Analysis":
    st.subheader("Income vs Loan Status")
    fig, ax = plt.subplots()
    sns.boxplot(x="Loan_Status", y="ApplicantIncome", data=df, ax=ax)
    st.pyplot(fig)

# Credit History
elif option == "Credit History":
    st.subheader("Credit History Impact")
    fig, ax = plt.subplots()
    sns.countplot(x="Credit_History", hue="Loan_Status", data=df, ax=ax)
    st.pyplot(fig)

# Property Area
elif option == "Property Area":
    st.subheader("Loan Approval by Property Area")
    fig, ax = plt.subplots()
    sns.countplot(x="Property_Area", hue="Loan_Status", data=df, ax=ax)
    st.pyplot(fig)

st.success("Streamlit App Running Successfully")
