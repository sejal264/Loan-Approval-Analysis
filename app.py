import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Loan Risk Assessment System",
                   layout="wide",
                   page_icon="💼")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("💼 Loan Approval Risk Assessment & Decision Support System")

# ---------------- SIDEBAR ----------------
st.sidebar.header("📂 Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

page = st.sidebar.radio("Navigation",
                        ["📊 Dashboard",
                         "🧠 Loan Decision System",
                         "💰 EMI Calculator"])

if file:

    df = pd.read_csv("LP_Train.csv")

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("🔍 Filters")

    gender_filter = st.sidebar.multiselect(
        "Select Gender",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    area_filter = st.sidebar.multiselect(
        "Select Property Area",
        options=df["Property_Area"].unique(),
        default=df["Property_Area"].unique()
    )

    df = df[(df["Gender"].isin(gender_filter)) &
            (df["Property_Area"].isin(area_filter))]

    # ================= DASHBOARD =================
    if page == "📊 Dashboard":

        st.subheader("📊 Data Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Applicants", len(df))
        col2.metric("Approved",
                    df[df["Loan_Status"] == "Y"].shape[0])
        col3.metric("Rejected",
                    df[df["Loan_Status"] == "N"].shape[0])
        col4.metric("Avg Income",
                    round(df["ApplicantIncome"].mean(), 2))

        st.markdown("---")

        col1, col2 = st.columns(2)

        fig1 = px.histogram(df,
                            x="ApplicantIncome",
                            title="Income Distribution")
        col1.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(df,
                      names="Loan_Status",
                      title="Loan Approval Ratio")
        col2.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(df,
                          x="ApplicantIncome",
                          y="LoanAmount",
                          color="Loan_Status",
                          title="Income vs Loan Amount")
        st.plotly_chart(fig3, use_container_width=True)

        # Download Button
        st.download_button("⬇ Download Filtered Data",
                           df.to_csv(index=False),
                           "filtered_data.csv",
                           "text/csv")

    # ================= LOAN DECISION =================
    elif page == "🧠 Loan Decision System":

        st.subheader("🧠 Smart Loan Eligibility Checker")

        income = st.number_input("Monthly Income (₹)")
        loan_amount = st.number_input("Loan Amount (₹)")
        credit = st.selectbox("Credit History (1=Good, 0=Bad)", [1, 0])

        if st.button("Check Eligibility"):

            risk_score = 0

            if income > 50000:
                risk_score += 40
            elif income > 30000:
                risk_score += 25
            else:
                risk_score += 10

            if credit == 1:
                risk_score += 40
            else:
                risk_score += 5

            if loan_amount < income * 5:
                risk_score += 20
            else:
                risk_score += 5

            st.progress(risk_score / 100)

            if risk_score >= 70:
                decision = "✅ Approved"
                category = "Low Risk"
            elif risk_score >= 40:
                decision = "⚠ Conditional Approval"
                category = "Medium Risk"
            else:
                decision = "❌ Rejected"
                category = "High Risk"

            st.success(f"Decision: {decision}")
            st.info(f"Risk Category: {category}")
            st.write(f"Risk Score: {risk_score}%")

    # ================= EMI CALCULATOR =================
    elif page == "💰 EMI Calculator":

        st.subheader("💰 EMI Calculator")

        loan = st.number_input("Loan Amount (₹)")
        rate = st.number_input("Interest Rate (%)")
        tenure = st.number_input("Tenure (Years)")

        if st.button("Calculate EMI"):

            if rate > 0 and tenure > 0:

                r = rate / (12 * 100)
                n = tenure * 12

                emi = (loan * r * (1 + r) ** n) / ((1 + r) ** n - 1)

                st.success(f"Monthly EMI: ₹ {round(emi, 2)}")
                st.write(f"Total Payment: ₹ {round(emi * n, 2)}")
                st.write(f"Total Interest: ₹ {round((emi * n) - loan, 2)}")

            else:
                st.error("Please enter valid Interest Rate & Tenure.")

else:
    st.warning("Please upload dataset to start the system.")
