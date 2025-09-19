import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from constants import (
    LOAN_AMOUNT, ANNUAL_INTEREST_RATE, TENURE_10_YEARS,
    TENURE_20_YEARS, SIP_ANNUAL_RETURN, SIP_DURATION_MONTHS
)
from report_utils import  generate_pdf

# --- Functions ---
def calculate_emi(principal, annual_rate, tenure_months):
    r = annual_rate / 12
    emi = (principal * r * (1 + r)**tenure_months) / ((1 + r)**tenure_months - 1)
    return round(emi, 2)

def calculate_sip_corpus(monthly_investment, monthly_rate, months):
    fv = monthly_investment * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    return round(fv, 2)

# --- Streamlit UI ---
st.set_page_config(page_title="Home Loan vs SIP Analyzer", layout="centered", initial_sidebar_state="expanded")

st.title("🏠 Home Loan vs SIP Analyzer")

st.markdown("""
This tool compares two scenarios for your home loan repayment:

1. **Full EMI Payment for 10 Years:** You pay higher EMIs and clear your loan in 10 years without investing in SIPs.

2. **Lower EMI Payment for 20 Years + SIP Investment:** You pay lower EMIs over 20 years and invest the EMI difference every month in SIPs to potentially build a corpus.

The analysis shows EMI amounts, total interest paid, monthly SIP amount (the difference), and SIP corpus growth over 20 years.
""")


# --- Sidebar Settings ---
with st.sidebar:
    # st.header("🔧 Settings")
    # dark_mode = st.toggle("🌙 Dark Mode", value=False)
    loan_amount = st.number_input("Loan Amount (Rs)", value=LOAN_AMOUNT, step=10000)
    interest_rate = st.slider("Home Loan Interest Rate (%)", 6.0, 12.0, ANNUAL_INTEREST_RATE * 100)
    sip_return = st.slider("Expected SIP Return (%)", 8.0, 15.0, SIP_ANNUAL_RETURN * 100)

# --- Calculations ---
emi_10 = calculate_emi(loan_amount, interest_rate / 100, TENURE_10_YEARS)
emi_20 = calculate_emi(loan_amount, interest_rate / 100, TENURE_20_YEARS)
monthly_sip = emi_10 - emi_20
sip_corpus = calculate_sip_corpus(monthly_sip, (sip_return / 100) / 12, SIP_DURATION_MONTHS)

total_interest_10 = round(emi_10 * TENURE_10_YEARS - loan_amount, 2)
total_interest_20 = round(emi_20 * TENURE_20_YEARS - loan_amount, 2)

# --- Output Metrics ---
st.subheader("📊 EMI & Interest Summary")
col1, col2 = st.columns(2)
col1.metric("EMI (10 Years)", f"Rs : {emi_10:,.2f}")
col2.metric("EMI (20 Years)", f"Rs : {emi_20:,.2f}")

col1.metric("Interest (10 Years)", f"Rs : {total_interest_10:,.2f}")
col2.metric("Interest (20 Years)", f"Rs : {total_interest_20:,.2f}")

st.success(f"💸 Monthly SIP: Rs {monthly_sip:,.2f}")
st.success(f"📈 SIP Corpus in 20 Years: Rs {sip_corpus:,.2f}")


# --- Graph: EMI vs SIP Growth ---
# st.subheader("📈 EMI vs SIP Growth Over Time")
st.subheader("📈 Comparison of Loan Payment vs Investment Growth Over Time")

st.markdown("""
This chart compares:

- **Total amount paid towards Home Loan EMIs over 10 years** (red dashed line)
- **Potential growth of monthly investments made by saving on EMIs by extending loan tenure to 20 years** (green solid line)

It shows how investing the EMI difference every month can grow your wealth over 20 years.
""")

months = np.arange(1, SIP_DURATION_MONTHS + 1)
sip_values = monthly_sip * (((1 + (sip_return / 100) / 12) ** months - 1) / ((sip_return / 100) / 12)) * (1 + (sip_return / 100) / 12)
emi_values = np.full_like(months, emi_10) * months

fig, ax = plt.subplots()

# Convert amounts to Lakhs
sip_values_lakh = sip_values / 1e5
emi_values_lakh = emi_values / 1e5

ax.plot(months / 12, sip_values_lakh, label="Accumulated SIP Investment Value (20 years)", color="green")
ax.plot(months / 12, emi_values_lakh, label="Cumulative EMI Paid (10 years)", linestyle="--", color="red")

ax.set_xlabel("Time (Years)")
ax.set_ylabel("Amount (Lakhs ₹)")
ax.set_title("Loan Payment vs SIP Investment Growth")
ax.legend()
ax.grid(True)

# Optional: Format y-axis ticks to show 1, 2, 3... with L suffix
import matplotlib.ticker as mtick

def lakh_formatter(x, pos):
    return f'{x:.1f}L'

ax.yaxis.set_major_formatter(mtick.FuncFormatter(lakh_formatter))

st.pyplot(fig)



# --- Downloads ---
st.subheader("⬇️ Download Reports")

results = {
    "EMI (10 Years)": f"Rs : {emi_10:,.2f}",
    "EMI (20 Years)": f"Rs : {emi_20:,.2f}",
    "Interest (10 Years)": f"Rs : {total_interest_10:,.2f}",
    "Interest (20 Years)": f"Rs : {total_interest_20:,.2f}",
    "Monthly SIP": f"Rs : {monthly_sip:,.2f}",
    "SIP Corpus (20 Years)": f"Rs : {sip_corpus:,.2f}",
}

col1, col2 = st.columns(2)
# with col1:
#     excel_data = generate_excel(results)
#     st.download_button("📊 Download Excel", data=excel_data, file_name="loan_vs_sip.xlsx", mime="application/vnd.ms-excel")

with col2:
    pdf_data = generate_pdf(results)
    st.download_button("📝 Download PDF", data=pdf_data, file_name="loan_vs_sip_report.pdf", mime="application/pdf")

st.caption("      Made with ❤️ by Nagesh Patil    ")
