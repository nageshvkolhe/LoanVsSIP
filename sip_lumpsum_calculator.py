import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="SIP & Lump Sum Calculator", layout="centered")

st.title("📈 SIP & Lump Sum Investment Calculator")

st.markdown("""
This tool helps you estimate the **future value** of your investments:

- 📅 **SIP (Monthly Investment)**: Investing a fixed amount every month.
- 💰 **Lump Sum**: Investing a one-time amount.

Choose the mode and enter your details to see potential returns.
""")

# --- Investment Mode ---
mode = st.radio("Select Investment Type", ["SIP", "Lump Sum"])

# --- Inputs ---
if mode == "SIP":
    monthly_investment = st.number_input("Monthly Investment (Rs)", value=5000, step=500)
    annual_return = st.slider("Expected Annual Return (%)", 6.0, 15.0, 12.0)
    years = st.slider("Investment Duration (Years)", 1, 30, 10)

    months = years * 12
    monthly_rate = annual_return / 12 / 100

    future_value = monthly_investment * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    total_invested = monthly_investment * months

else:  # Lump Sum
    lump_sum = st.number_input("Lump Sum Amount (Rs)", value=100000, step=10000)
    annual_return = st.slider("Expected Annual Return (%)", 6.0, 15.0, 12.0)
    years = st.slider("Investment Duration (Years)", 1, 30, 10)

    future_value = lump_sum * (1 + annual_return / 100)**years
    total_invested = lump_sum

# --- Output ---
st.subheader("📊 Results")
st.metric("Total Invested", f"₹ {total_invested:,.2f}")
st.metric("Estimated Value", f"₹ {future_value:,.2f}")
st.metric("Wealth Gained", f"₹ {future_value - total_invested:,.2f}")

# --- Chart ---
st.subheader("📈 Investment Growth Over Time")

years_range = np.arange(1, years + 1)

if mode == "SIP":
    monthly_rate = annual_return / 12 / 100
    values = [monthly_investment * (((1 + monthly_rate)**(yr * 12) - 1) / monthly_rate) * (1 + monthly_rate) for yr in years_range]
else:
    values = [lump_sum * (1 + annual_return / 100)**yr for yr in years_range]

values_lakh = np.array(values) / 1e5  # in Lakhs

fig, ax = plt.subplots()
ax.plot(years_range, values_lakh, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Value (Lakhs ₹)")
ax.set_title(f"{mode} Growth Over Time")
ax.grid(True)

st.pyplot(fig)

st.caption("🧮 Built by Nagesh Patil")
