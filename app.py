import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Loan Risk Analyzer", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
💼 AI Loan Risk & Approval Intelligence System
</h1>
<p style='text-align: center;'>Smart Financial Decision Support Dashboard</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", 
                       ["📊 Dashboard", "🧠 Smart Loan Analyzer", "💰 EMI Planner"])

st.sidebar.markdown("---")
st.sidebar.header("📂 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# ---------------- DATA LOAD ----------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.fillna(df.median(numeric_only=True), inplace=True)
    return df

if file:
    df = load_data(file)

    # ---------------- DASHBOARD ----------------
    if page == "📊 Dashboard":

        st.subheader("📊 Business Insights Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Applicants", len(df))
        col2.metric("Approved", df[df["Loan_Status"]=="Y"].shape[0])
        col3.metric("Rejected", df[df["Loan_Status"]=="N"].shape[0])
        col4.metric("Avg Income", int(df["ApplicantIncome"].mean()))

        st.markdown("---")

        # Filters
        st.subheader("🔍 Filter Data")
        status_filter = st.selectbox("Loan Status", ["All","Y","N"])

        filtered_df = df.copy()
        if status_filter != "All":
            filtered_df = df[df["Loan_Status"]==status_filter]

        col1, col2 = st.columns(2)

        fig1 = px.histogram(filtered_df, x="ApplicantIncome", 
                            title="Income Distribution", nbins=30)
        col1.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(filtered_df, names="Loan_Status", 
                      title="Approval Ratio")
        col2.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(filtered_df,
                          x="ApplicantIncome",
                          y="LoanAmount",
                          color="Loan_Status",
                          size="LoanAmount",
                          title="Income vs Loan (Risk Pattern)")
        st.plotly_chart(fig3, use_container_width=True)

        # Insights
        st.markdown("### 📌 Key Insights")
        st.info("Higher income + good credit history → higher approval chances")

    # ---------------- SMART ANALYZER ----------------
    elif page == "🧠 Smart Loan Analyzer":

        st.subheader("🧠 AI-Based Loan Risk Analyzer")

        col1, col2 = st.columns(2)

        income = col1.number_input("Monthly Income", 1000, 1000000)
        loan = col2.number_input("Loan Amount", 1000, 1000000)
        credit = st.selectbox("Credit History", ["Good","Bad"])
        dependents = st.slider("Dependents", 0, 5, 1)

        if st.button("Analyze Application"):

            score = 0

            if income > 50000:
                score += 30
            elif income > 25000:
                score += 20
            else:
                score += 10

            if loan < income * 4:
                score += 30
            else:
                score += 10

            if credit == "Good":
                score += 30
            else:
                score += 5

            if dependents <= 2:
                score += 10

            # Risk Decision
            if score >= 80:
                decision = "✅ Approved"
                risk = "Low Risk"
                color = "green"
            elif score >= 50:
                decision = "⚠️ Conditional"
                risk = "Medium Risk"
                color = "orange"
            else:
                decision = "❌ Rejected"
                risk = "High Risk"
                color = "red"

            st.markdown(f"### 🎯 Decision: {decision}")
            st.markdown(f"### 📊 Risk Level: {risk}")
            st.progress(score/100)

            st.markdown("### 📌 Explanation")
            st.write("Decision is based on income strength, loan ratio, credit behavior and dependents.")

    # ---------------- EMI ----------------
    elif page == "💰 EMI Planner":

        st.subheader("💰 Smart EMI Calculator")

        loan = st.number_input("Loan Amount", 1000, 1000000)
        rate = st.slider("Interest Rate (%)", 1.0, 20.0)
        tenure = st.slider("Years", 1, 30)

        if st.button("Calculate EMI"):

            r = rate/(12*100)
            n = tenure*12

            emi = (loan*r*(1+r)**n)/((1+r)**n-1)

            st.success(f"Monthly EMI: ₹ {round(emi,2)}")

            total = emi*n
            interest = total - loan

            col1, col2 = st.columns(2)
            col1.metric("Total Payment", int(total))
            col2.metric("Total Interest", int(interest))

            fig = px.pie(values=[loan, interest],
                         names=["Principal","Interest"],
                         title="Payment Breakdown")
            st.plotly_chart(fig)

else:
    st.warning("📂 Upload dataset to start")
