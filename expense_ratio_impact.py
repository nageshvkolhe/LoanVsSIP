import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Streamlit Config ---
st.set_page_config(page_title="Expense Ratio Impact", layout="centered")

st.title("📉 Impact of Expense Ratio on Investment Returns")

st.markdown("""
Understand how **Expense Ratio** affects your **mutual fund returns** over time. Even small differences in expense ratios can significantly impact your corpus over the long term.

This calculator compares:
- 📈 **Without Expense Ratio** (Gross Return)
- 🧾 **With Expense Ratio** (Net Return)
""")

# --- Inputs ---
investment = st.number_input("💰 Initial Investment (Rs)", value=1000000, step=10000)
annual_return = st.slider("📊 Expected Annual Return (%)", 8.0, 15.0, 12.0)
expense_ratio = st.slider(
    "🧾 Expense Ratio (%)",
    min_value=0.1,
    max_value=3.0,
    value=0.1,
    step=0.01
)

years = st.slider("⏳ Investment Duration (Years)", 1, 30, 10)

# --- Calculations ---
gross_rate = annual_return / 100
net_rate = (annual_return - expense_ratio) / 100

future_value_gross = investment * ((1 + gross_rate) ** years)
future_value_net = investment * ((1 + net_rate) ** years)
loss_due_to_expense = future_value_gross - future_value_net

# --- Display Results ---
st.subheader("📊 Comparison Summary")
col1, col2 = st.columns(2)
col1.metric("Future Value (Gross)", f"₹ {future_value_gross:,.2f}")
col2.metric("Future Value (Net)", f"₹ {future_value_net:,.2f}")

st.warning(f"💸 Loss due to Expense Ratio: ₹ {loss_due_to_expense:,.2f}")

# --- Chart ---
st.subheader("📈 Corpus Growth Over Time")

years_range = np.arange(1, years + 1)
gross_values = investment * ((1 + gross_rate) ** years_range)
net_values = investment * ((1 + net_rate) ** years_range)

fig, ax = plt.subplots()
ax.plot(years_range, gross_values / 1e5, label="Without Expense Ratio", linestyle="--", color="green")
ax.plot(years_range, net_values / 1e5, label="With Expense Ratio", color="red")
ax.set_xlabel("Years")
ax.set_ylabel("Value (Lakhs ₹)")
ax.set_title("Growth With vs Without Expense Ratio")
ax.grid(True)
ax.legend()

st.pyplot(fig)

st.caption("🔍 Created by Nagesh Patil")
