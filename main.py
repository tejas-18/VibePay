import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
import json
from dotenv import load_dotenv
import altair as alt

# Load environment variables
load_dotenv()

# Set page config MUST be the first Streamlit command
st.set_page_config(page_title="VibePay", page_icon="💸", layout="wide")

# Custom CSS for a premium feel
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    .sub-header {
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #FF416C;
        font-weight: 700;
    }
    /* Style the form border */
    [data-testid="stForm"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Please set GOOGLE_API_KEY in your .env file.")

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Vendor", "Category", "Amount"])

# System instruction
system_instruction = """
You are an intelligent expense tracker assistant.
Extract the expense details from the user's input and return a JSON object with exactly these keys:
- Amount (number)
- Category (string: e.g., Food, Transport, Rent, Entertainment, Utilities, Shopping, Other)
- Vendor (string)
- Date (string in YYYY-MM-DD format, default to today if not mentioned)

Respond ONLY with valid JSON. Do not include any markdown formatting like ```json.
"""

def extract_expense_details(text):
    if not api_key:
         return None
    try:
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
        response = model.generate_content(text)
        
        response_text = response.text.strip()
        if response_text.startswith("```json"):
             response_text = response_text[7:]
        if response_text.startswith("```"):
             response_text = response_text[3:]
        if response_text.endswith("```"):
             response_text = response_text[:-3]
             
        return json.loads(response_text.strip())
    except Exception as e:
        st.error(f"Error parsing input: {e}")
        return None

# Sidebar for functionality
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Manage your VibePay data.")
    st.markdown("---")
    if st.button("🗑️ Clear All Expenses", use_container_width=True, type="primary"):
        st.session_state.expenses = pd.DataFrame(columns=["Date", "Vendor", "Category", "Amount"])
        st.success("Expenses cleared!")

# App UI Header
st.markdown('<p class="main-header">💸 VibePay</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your AI-powered natural language expense tracker. Just type what you spent!</p>', unsafe_allow_html=True)

# Input form
with st.form("expense_form", clear_on_submit=True):
    user_input = st.text_input("What did you spend on?", placeholder="e.g., Grabbed some groceries from D-Mart for 450 rupees")
    submitted = st.form_submit_button("Track Expense", use_container_width=True)
    
    if submitted and user_input:
        with st.spinner("✨ Analyzing your expense..."):
            expense_data = extract_expense_details(user_input)
            if expense_data:
                new_row = pd.DataFrame([expense_data])
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_row], ignore_index=True)
                st.toast(f"Added {expense_data['Category']} expense for ₹{expense_data['Amount']}!")

# Display Data Dashboard
if not st.session_state.expenses.empty:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Data Prep
    df = st.session_state.expenses.copy()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    total_spent = df["Amount"].sum()
    highest_expense = df.loc[df["Amount"].idxmax()]
    
    # --- METRICS ROW ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Spent", f"₹{total_spent:,.2f}")
    with col2:
        st.metric("🧾 Transactions", len(df))
    with col3:
        st.metric("🔥 Highest Expense", f"₹{highest_expense['Amount']:,.2f}", highest_expense['Category'], delta_color="inverse")
        
    st.markdown("---")
    
    # --- CHARTS & DATA ROW ---
    col_chart, col_table = st.columns([1.2, 1])
    
    with col_chart:
        st.subheader("📊 Spending by Category")
        category_totals = df.groupby("Category", as_index=False)["Amount"].sum()
        
        # Beautiful Modern Donut Chart with Custom VibePay Colors
        custom_colors = ['#FF416C', '#FF4B2B', '#FF8E53', '#833AB4', '#C13584', '#3b82f6', '#10b981', '#f59e0b']
        
        chart = alt.Chart(category_totals).mark_arc(
            innerRadius=70, 
            cornerRadius=8, 
            padAngle=0.04
        ).encode(
            theta=alt.Theta(field="Amount", type="quantitative"),
            color=alt.Color(
                field="Category", 
                type="nominal", 
                scale=alt.Scale(range=custom_colors), 
                legend=alt.Legend(
                    title="", 
                    orient="bottom", 
                    labelFontSize=13, 
                    symbolType="circle",
                    columns=2
                )
            ),
            tooltip=[
                alt.Tooltip('Category', title='Category'),
                alt.Tooltip('Amount', title='Amount (₹)', format=',.2f')
            ]
        ).properties(
            height=380
        ).configure_view(strokeWidth=0)
        
        st.altair_chart(chart, use_container_width=True)

    with col_table:
        st.subheader("📝 Recent Transactions")
        st.dataframe(
            df.sort_values(by="Date", ascending=False), 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "Date": st.column_config.DateColumn("Date")
            }
        )
else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👋 No expenses tracked yet. Enter one above to see your interactive dashboard!")
