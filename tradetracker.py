
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Trade Tracker", layout="wide")
st.title("📊 Options Trade Tracker")

LOG_FILE = "trade_log.csv"

# --- Load existing trades ---
@st.cache_data
def load_trades():
    try:
        return pd.read_csv(LOG_FILE, parse_dates=["Open_Date", "Close_Date"])
    except:
        return pd.DataFrame(columns=[
            "Order #", "Symbol", "Open_Date", "Close_Date", "Total_Value",
            "Trade_Count", "Days_Held", "Result"
        ])

trades_df = load_trades()

# --- Display trades ---
st.subheader("📈 Trade History")
if not trades_df.empty:
    def highlight_result(val):
        color = {
            'Win': 'green',
            'Loss': 'red',
            'Break-even': 'gray'
        }.get(val, 'white')
        return f'background-color: {color}; color: white'

    st.dataframe(
        trades_df.style.applymap(highlight_result, subset=["Result"]),
        use_container_width=True
    )
else:
    st.info("No trades logged yet.")

# --- Add new trade ---
st.subheader("➕ Add New Trade")
with st.form("add_trade"):
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.text_input("Symbol (e.g., SPY)", max_chars=10)
        order_id = st.text_input("Order #")
        result = st.selectbox("Result", ["Win", "Loss", "Break-even"])
        total_value = st.number_input("P/L Value ($)", value=0.00, step=0.01)
    with col2:
        open_date = st.date_input("Open Date", value=date.today())
        close_date = st.date_input("Close Date", value=date.today())
        trade_count = st.number_input("Number of legs (1-4 typical)", value=1, step=1)

    submitted = st.form_submit_button("Add Trade")

    if submitted:
        new_trade = pd.DataFrame([{
            "Order #": order_id,
            "Symbol": symbol.upper(),
            "Open_Date": pd.to_datetime(open_date),
            "Close_Date": pd.to_datetime(close_date),
            "Total_Value": total_value,
            "Trade_Count": trade_count,
            "Days_Held": (close_date - open_date).days,
            "Result": result
        }])
        updated_df = pd.concat([trades_df, new_trade], ignore_index=True)
        updated_df.to_csv(LOG_FILE, index=False)
        st.success("Trade added! Please reload the app to see the updated table.")

# --- Download link ---
st.download_button(
    "📥 Download Trade Log CSV",
    data=trades_df.to_csv(index=False),
    file_name="trade_log.csv",
    mime="text/csv"
)
