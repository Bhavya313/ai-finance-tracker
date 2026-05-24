import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
from datetime import datetime, date
import calendar
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

st.set_page_config(page_title="🌸 Finance Diary", page_icon="🌸", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Dancing+Script:wght@700&display=swap');

* { font-family: 'Nunito', sans-serif !important; color: #333333; }

.stApp {
    background: linear-gradient(160deg, #f0faf8 0%, #e0f7f4 50%, #f0faf8 100%) !important;
}

/* Fix dark mode */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #f0faf8 0%, #e0f7f4 50%, #f0faf8 100%) !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] div,
[data-testid="stMarkdownContainer"] span {
    color: #333333 !important;
}
.stSelectbox label, .stNumberInput label,
.stTextInput label, .stDateInput label,
.stForm label { color: #333333 !important; }
[data-testid="stMetricValue"] { color: #333333 !important; }
[data-testid="stMetricLabel"] { color: #666666 !important; }
p, span, div, label { color: #333333; }

.main-header {
    background: linear-gradient(135deg, #00b894, #00897b);
    border-radius: 28px;
    padding: 28px 20px;
    text-align: center;
    color: white !important;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,184,148,0.4);
}
.main-header h1 {
    font-family: 'Dancing Script', cursive !important;
    font-size: 2.8em !important;
    margin: 0 !important;
    color: white !important;
}
.main-header p { margin: 6px 0 0 0; opacity: 0.9; color: white !important; }

.metric-row { display: flex; gap: 10px; margin: 15px 0; }
.metric-card {
    flex: 1; background: white; border-radius: 20px;
    padding: 16px 12px; text-align: center;
    box-shadow: 0 4px 15px rgba(0,184,148,0.12);
}
.metric-card .val { font-size: 1.4em; font-weight: 900; }
.metric-card .lbl { font-size: 0.75em; color: #888; margin-top: 4px; font-weight: 600; }
.income-val { color: #2ecc71 !important; }
.expense-val { color: #00b894 !important; }
.balance-val { color: #00897b !important; }

.cat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0; }
.cat-card {
    background: white; border-radius: 18px; padding: 14px 10px;
    text-align: center; box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    cursor: pointer; transition: transform 0.2s;
}
.cat-card:hover { transform: translateY(-2px); }
.cat-name { font-size: 0.75em; color: #888 !important; font-weight: 700; }
.cat-amount { font-size: 1.1em; font-weight: 900; color: #333 !important; margin: 4px 0; }
.cat-bar { height: 4px; border-radius: 2px; margin-top: 6px; }

.tx-row {
    background: white; border-radius: 14px; padding: 12px 16px; margin: 6px 0;
    display: flex; justify-content: space-between; align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.tx-expense { color: #00b894 !important; font-weight: 900; font-size: 1.05em; }
.tx-income  { color: #2ecc71 !important; font-weight: 900; font-size: 1.05em; }

.calc-display {
    background: linear-gradient(135deg, #00b894, #00897b);
    border-radius: 20px; padding: 20px; text-align: center;
    color: white !important; margin-bottom: 15px;
}
.calc-amount { font-size: 3em; font-weight: 900; color: white !important; }

.cal-header {
    background: linear-gradient(135deg, #00b894, #00897b);
    border-radius: 18px; padding: 15px;
    color: white !important; text-align: center; margin-bottom: 15px;
}

.goal-card {
    background: white; border-radius: 20px; padding: 18px; margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0,184,148,0.12);
    border: 2px solid rgba(0,184,148,0.1);
}

.alert-pink {
    background: #f0faf8; border-left: 4px solid #00b894;
    border-radius: 12px; padding: 12px 16px;
    margin: 8px 0; color: #006b50 !important; font-weight: 600;
}
.alert-purple {
    background: #e0f7f4; border-left: 4px solid #00897b;
    border-radius: 12px; padding: 12px 16px;
    margin: 8px 0; color: #004d40 !important; font-weight: 600;
}
.alert-green {
    background: #f0fff8; border-left: 4px solid #2ecc71;
    border-radius: 12px; padding: 12px 16px;
    margin: 8px 0; color: #006b38 !important; font-weight: 600;
}

.section-title {
    font-family: 'Dancing Script', cursive !important;
    font-size: 1.6em; color: #00897b !important; margin: 18px 0 10px 0;
}

.currency-badge {
    background: linear-gradient(135deg, #00b894, #00897b);
    color: white !important; border-radius: 20px;
    padding: 4px 12px; font-size: 0.85em; font-weight: 700;
    display: inline-block; margin-left: 8px;
}

.stButton > button {
    background: linear-gradient(135deg, #00b894, #00897b) !important;
    color: white !important; border: none !important;
    border-radius: 14px !important; font-weight: 700 !important;
    font-size: 0.95em !important; padding: 10px 20px !important;
    box-shadow: 0 4px 15px rgba(0,184,148,0.3) !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #00b894, #00897b) !important;
    border-radius: 10px !important;
}
div[data-testid="metric-container"] {
    background: white; border-radius: 18px;
    padding: 15px; border-top: 4px solid #00b894;
    box-shadow: 0 4px 15px rgba(0,184,148,0.1);
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.9);
    border-radius: 16px; padding: 4px; gap: 2px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00b894, #00897b) !important;
    color: white !important; border-radius: 12px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important; font-weight: 700 !important;
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🌸 Finance Diary</h1>
    <p>Your cute & smart money tracker ✨</p>
</div>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────
defaults = {
    "expenses": [], "income_entries": [],
    "monthly_income": 0.0, "chat_history": [],
    "budgets": {c: 0.0 for c in [
        "Food & Dining","Transport","Shopping","Entertainment",
        "Bills & Utilities","Health","Education","Others"
    ]},
    "bills": [], "goals": [],
    "calc_amount": "10", "quick_cat": "Food & Dining",
    "edit_idx": None, "show_success": None,
    "currency": "USD $", "active_tab": None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "llm" not in st.session_state:
    st.session_state.llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_KEY")
    )

# Currency setup
CURRENCY_OPTIONS = {
    "USD $": "$",
    "INR ₹": "₹",
    "EUR €": "€",
    "GBP £": "£",
    "JPY ¥": "¥",
    "AUD $": "A$",
    "CAD $": "C$",
}
SYMBOL = CURRENCY_OPTIONS.get(st.session_state.currency, "$")

CATEGORIES = ["Food & Dining","Transport","Shopping","Entertainment",
              "Bills & Utilities","Health","Education","Others"]
CAT_ICONS  = {"Food & Dining":"🍜","Transport":"🚗","Shopping":"🛍️",
              "Entertainment":"🎬","Bills & Utilities":"💡",
              "Health":"💊","Education":"📚","Others":"✨"}
CAT_COLORS = {"Food & Dining":"#FFD580","Transport":"#A8D8FF",
              "Shopping":"#FFB3D1","Entertainment":"#D4A8FF",
              "Bills & Utilities":"#A8FFD4","Health":"#FFB3B3",
              "Education":"#B3D4FF","Others":"#E8E8E8"}
GREEN = ["#00b894","#00897b","#55efc4","#81ecec",
         "#a8e6cf","#dfe6e9","#b2dfdb","#e0f7fa"]

def total_spent():
    return sum(e["amount"] for e in st.session_state.expenses)

def cat_spending():
    if not st.session_state.expenses:
        return {}
    df = pd.DataFrame(st.session_state.expenses)
    return df.groupby("category")["amount"].sum().to_dict()

def get_alerts():
    alerts = []
    cs = cat_spending()
    for cat, lim in st.session_state.budgets.items():
        if lim > 0:
            sp  = cs.get(cat, 0)
            pct = sp / lim * 100
            if sp > lim:
                alerts.append(("pink", f"🚨 Budget Alert: {CAT_ICONS.get(cat,'')} {cat} exceeded! Spent {SYMBOL}{sp:.0f} of {SYMBOL}{lim:.0f} limit"))
            elif pct >= 80:
                alerts.append(("purple", f"⚠️ Budget Warning: {CAT_ICONS.get(cat,'')} {cat} is {pct:.0f}% used ({SYMBOL}{sp:.0f} / {SYMBOL}{lim:.0f})"))
    today = date.today()
    for b in st.session_state.bills:
        if not b["paid"]:
            due = datetime.strptime(b["due_date"], "%Y-%m-%d").date()
            dl  = (due - today).days
            if dl < 0:
                alerts.append(("pink", f"🚨 Bill Overdue: {b['name']} — {SYMBOL}{b['amount']:.0f} was due {abs(dl)} day(s) ago!"))
            elif dl <= 3:
                alerts.append(("purple", f"⏰ Bill Due Soon: {b['name']} — {SYMBOL}{b['amount']:.0f} due in {dl} day(s)"))
    for g in st.session_state.goals:
        due  = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
        dl   = (due - today).days
        pct  = (g["saved"] / g["target"] * 100) if g["target"] > 0 else 0
        if dl < 0 and pct < 100:
            alerts.append(("pink", f"🚨 Goal Overdue: {g.get('emoji','🌸')} {g['name']} deadline passed! Only {pct:.0f}% saved"))
        elif dl <= 7 and pct < 100:
            alerts.append(("purple", f"⏰ Goal Deadline Soon: {g.get('emoji','🌸')} {g['name']} — {dl} days left! {pct:.0f}% saved"))
        elif pct >= 100:
            alerts.append(("green", f"🎉 Goal Completed: {g.get('emoji','🌸')} {g['name']} — You did it! 💜"))
    return alerts

# Global alerts
all_alerts = get_alerts()
if all_alerts:
    for atype, msg in all_alerts:
        cls = "alert-pink" if atype == "pink" else "alert-purple" if atype == "purple" else "alert-green"
        st.markdown(f'<div class="{cls}">🔔 {msg}</div>', unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Home","⚡ Log","📅 Calendar",
    "📊 Charts","🎯 Budget","🌟 Goals","🤖 AI"
])

# ════════════════════════════════════════
# TAB 1 — HOME
# ════════════════════════════════════════
with tab1:
    # Currency selector
    col_c1, col_c2 = st.columns([3, 1])
    with col_c1:
        income = st.number_input(
            f"💵 Monthly Income ({SYMBOL})",
            min_value=0.0,
            value=st.session_state.monthly_income,
            step=100.0)
        st.session_state.monthly_income = income
    with col_c2:
        selected_currency = st.selectbox(
            "💱 Currency",
            list(CURRENCY_OPTIONS.keys()),
            index=list(CURRENCY_OPTIONS.keys()).index(
                st.session_state.currency))
        if selected_currency != st.session_state.currency:
            st.session_state.currency = selected_currency
            st.rerun()

    spent   = total_spent()
    balance = income - spent
    pct     = (balance / income * 100) if income > 0 else 0

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="val income-val">{SYMBOL}{income:,.0f}</div>
            <div class="lbl">💵 Income</div>
        </div>
        <div class="metric-card">
            <div class="val expense-val">{SYMBOL}{spent:,.0f}</div>
            <div class="lbl">💸 Spent</div>
        </div>
        <div class="metric-card">
            <div class="val balance-val">{SYMBOL}{balance:,.0f}</div>
            <div class="lbl">💰 Balance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Category cards — tap to go to Log tab
   # Category buttons that look like cards
    st.markdown('<div class="section-title">💸 Tap Category to Log</div>',
               unsafe_allow_html=True)
    cs = cat_spending()

    # Add CSS for card-style buttons
    st.markdown("""
    <style>
    div[data-testid="column"] .stButton > button {
        background: white !important;
        color: #333 !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 14px 8px !important;
        width: 100% !important;
        height: 100px !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.07) !important;
        font-size: 0.8em !important;
        font-weight: 700 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s !important;
    }
    div[data-testid="column"] .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0,184,148,0.2) !important;
        border: 2px solid #00b894 !important;
        color: #00897b !important;
    }
    </style>
    """, unsafe_allow_html=True)

    cat_cols = st.columns(4)
    for i, cat in enumerate(CATEGORIES):
        sp = cs.get(cat, 0)
        icon = CAT_ICONS[cat]
        color = CAT_COLORS[cat]
        with cat_cols[i % 4]:
            st.markdown(f"""
            <div style="background:{color}; border-radius:14px;
                        padding:8px; text-align:center; margin-bottom:4px;
                        font-size:1.6em">{icon}</div>
            """, unsafe_allow_html=True)
            if st.button(
                f"{cat.split(' & ')[0].split(' ')[0]}\n{SYMBOL}{sp:.0f}",
                key=f"home_cat_{cat}"):
                st.session_state.quick_cat = cat
                st.session_state.active_tab = "log"
                st.rerun()

    # Recent transactions
    if st.session_state.expenses:
        st.markdown('<div class="section-title">🧾 Recent Transactions</div>',
                   unsafe_allow_html=True)

        recent_indices = sorted(range(len(st.session_state.expenses)),
                                key=lambda i: st.session_state.expenses[i]["date"],
                                reverse=True)[:15]
        by_date = {}
        for i in recent_indices:
            e = st.session_state.expenses[i]
            by_date.setdefault(e["date"], []).append((i, e))

        for d, txs in sorted(by_date.items(), reverse=True):
            dt        = datetime.strptime(d, "%Y-%m-%d")
            dow       = dt.strftime("%A")
            day_total = sum(e["amount"] for _, e in txs)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; margin:15px 0 8px 0">
                <div style="background:linear-gradient(135deg,#00b894,#00897b);
                            color:white; border-radius:50%; width:38px; height:38px;
                            display:flex; align-items:center; justify-content:center;
                            font-weight:900; font-size:0.95em">{dt.day}</div>
                <span style="font-family:'Dancing Script',cursive; font-size:1.3em;
                             color:#00897b">{dow}</span>
                <span style="margin-left:auto; color:#00b894; font-weight:700">
                    OUT {SYMBOL}{day_total:.0f}
                </span>
            </div>
            """, unsafe_allow_html=True)

            for idx, tx in txs:
                icon  = CAT_ICONS.get(tx["category"], "✨")
                color = CAT_COLORS.get(tx["category"], "#eee")

                if st.session_state.edit_idx == idx:
                    with st.form(f"edit_form_{idx}"):
                        st.markdown("**✏️ Edit Transaction**")
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            new_desc = st.text_input("Description", value=tx["description"])
                            new_date = st.date_input("Date",
                                value=datetime.strptime(tx["date"], "%Y-%m-%d"))
                        with ec2:
                            new_amount = st.number_input(f"Amount ({SYMBOL})",
                                min_value=0.01, value=tx["amount"], step=0.5)
                            new_cat = st.selectbox("Category", CATEGORIES,
                                index=CATEGORIES.index(tx["category"])
                                if tx["category"] in CATEGORIES else 0)
                        sc1, sc2 = st.columns(2)
                        with sc1:
                            if st.form_submit_button("💾 Save", use_container_width=True):
                                st.session_state.expenses[idx] = {
                                    "date": str(new_date),
                                    "category": new_cat,
                                    "description": new_desc,
                                    "amount": new_amount
                                }
                                st.session_state.edit_idx = None
                                st.success("🌸 Updated!")
                                st.rerun()
                        with sc2:
                            if st.form_submit_button("❌ Cancel", use_container_width=True):
                                st.session_state.edit_idx = None
                                st.rerun()
                else:
                    st.markdown(f"""
                    <div class="tx-row">
                        <div style="display:flex; align-items:center">
                            <div style="background:{color}; border-radius:12px;
                                        width:38px; height:38px; display:flex;
                                        align-items:center; justify-content:center;
                                        font-size:1.2em; margin-right:10px">{icon}</div>
                            <div>
                                <div style="font-weight:700; font-size:0.95em; color:#333">
                                    {tx['description']}
                                </div>
                                <div style="color:#aaa; font-size:0.78em">
                                    {tx['category']} · {tx['date']}
                                </div>
                            </div>
                        </div>
                        <div class="tx-expense">{SYMBOL}{tx['amount']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{idx}"):
                            st.session_state.edit_idx = idx
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Delete", key=f"del_{idx}"):
                            st.session_state.expenses.pop(idx)
                            st.success("🌸 Deleted!")
                            st.rerun()

        st.markdown("---")
        if st.button("🗑️ Clear All Expenses"):
            st.session_state.expenses = []
            st.rerun()
    else:
        st.markdown(f"""
        <div style="background:white; border-radius:20px; padding:30px;
                    text-align:center; box-shadow:0 4px 15px rgba(0,184,148,0.1)">
            <div style="font-size:2.5em">🌸</div>
            <div style="color:#00897b; font-weight:700; margin-top:8px">
                No transactions yet!<br>
                <small style="color:#aaa">Tap a category above to log your first expense</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 2 — QUICK LOG
# ════════════════════════════════════════
with tab2:
    # Auto scroll here if coming from category click
    if st.session_state.get("active_tab") == "log":
        st.session_state.active_tab = None
        st.markdown(f"""
        <div class="alert-green">
            ✅ Category selected: 
            <strong>{CAT_ICONS.get(st.session_state.quick_cat,'')} 
            {st.session_state.quick_cat}</strong> — Fill in the details below!
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚡ Quick Log</div>', unsafe_allow_html=True)

    if st.session_state.get("show_success"):
        st.success(f"🌸 Successfully logged — {st.session_state.show_success}!")
        st.session_state.show_success = None

    # Calculator display
    st.markdown(f"""
    <div class="calc-display">
        <div style="font-size:0.85em; opacity:0.85; font-weight:700; color:white">
            {CAT_ICONS.get(st.session_state.quick_cat,'')}
            {st.session_state.quick_cat}
        </div>
        <div class="calc-amount">
            {SYMBOL}{float(st.session_state.calc_amount or 0):,.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clear amount button
    col_clr1, col_clr2 = st.columns([1, 3])
    with col_clr1:
        if st.button("🗑️ Clear Amount"):
            st.session_state.calc_amount = "0"
            st.rerun()

    # Quick amount buttons
    st.markdown(f"**{SYMBOL} Quick Amounts:**")
    qcols = st.columns(5)
    for i, amt in enumerate([5, 10, 20, 50, 100]):
        with qcols[i]:
            if st.button(f"{SYMBOL}{amt}", key=f"qa_{amt}"):
                st.session_state.calc_amount = str(float(amt))
                st.rerun()

    # Category buttons
    st.markdown("**📂 Category:**")
    cat_cols = st.columns(4)
    for i, cat in enumerate(CATEGORIES):
        with cat_cols[i % 4]:
            icon  = CAT_ICONS[cat]
            label = cat.split(' & ')[0].split(' ')[0]
            is_selected = st.session_state.quick_cat == cat
            if st.button(f"{icon} {label}", key=f"qc_{cat}",
                        type="primary" if is_selected else "secondary"):
                st.session_state.quick_cat = cat
                st.rerun()

    st.markdown(f"""
    <div class="alert-green" style="margin:10px 0">
        ✅ Selected: <strong>{CAT_ICONS.get(st.session_state.quick_cat,'')}
        {st.session_state.quick_cat}</strong>
    </div>
    """, unsafe_allow_html=True)

    # Log form
    with st.form("quick_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            q_desc = st.text_input("📝 Description",
                                   placeholder="e.g. Coffee, Uber, Lunch")
            q_date = st.date_input("📅 Date", value=datetime.today())
        with col2:
            q_amount = st.number_input(f"💵 Amount ({SYMBOL})", min_value=0.01,
                                       step=0.5,
                                       value=max(float(
                                           st.session_state.calc_amount or 10), 0.01))
            q_type = st.selectbox("📌 Type", ["Expense", "Income"])

        if st.form_submit_button("✨ Log it!", use_container_width=True):
            if q_desc:
                if q_type == "Expense":
                    st.session_state.expenses.append({
                        "date": str(q_date),
                        "category": st.session_state.quick_cat,
                        "description": q_desc,
                        "amount": q_amount
                    })
                else:
                    st.session_state.income_entries.append({
                        "date": str(q_date),
                        "description": q_desc,
                        "amount": q_amount
                    })
                st.session_state.calc_amount = "10"
                st.session_state.show_success = q_desc
                st.rerun()
            else:
                st.error("Please add a description!")

    # Today's summary
    today_str = str(date.today())
    today_exp = [e for e in st.session_state.expenses if e["date"] == today_str]
    today_inc = [e for e in st.session_state.income_entries if e["date"] == today_str]
    if today_exp or today_inc:
        te = sum(e["amount"] for e in today_exp)
        ti = sum(e["amount"] for e in today_inc)
        st.markdown(f"""
        <div style="background:white; border-radius:18px; padding:16px;
                    text-align:center; margin-top:15px;
                    box-shadow:0 4px 15px rgba(0,184,148,0.1)">
            <div style="color:#aaa; font-size:0.85em; font-weight:700">Today</div>
            <div style="display:flex; justify-content:center; gap:30px; margin-top:8px">
                <div>
                    <div style="color:#00b894; font-size:1.4em; font-weight:900">
                        -{SYMBOL}{te:.2f}
                    </div>
                    <div style="color:#aaa; font-size:0.75em">OUT</div>
                </div>
                <div>
                    <div style="color:#2ecc71; font-size:1.4em; font-weight:900">
                        +{SYMBOL}{ti:.2f}
                    </div>
                    <div style="color:#aaa; font-size:0.75em">IN</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 3 — CALENDAR
# ════════════════════════════════════════
with tab3:
    today = date.today()
    col1, col2 = st.columns(2)
    with col1:
        cal_month = st.selectbox("Month", range(1, 13),
                                  index=today.month - 1,
                                  format_func=lambda x: calendar.month_name[x])
    with col2:
        cal_year = st.selectbox("Year", [2024, 2025, 2026], index=2)

    mo_exp = [e for e in st.session_state.expenses
              if e["date"].startswith(f"{cal_year}-{cal_month:02d}")]
    mo_inc = [e for e in st.session_state.income_entries
              if e["date"].startswith(f"{cal_year}-{cal_month:02d}")]
    mo_exp_total = sum(e["amount"] for e in mo_exp)
    mo_inc_total = sum(e["amount"] for e in mo_inc) + (
        st.session_state.monthly_income if not st.session_state.income_entries else 0)
    mo_bal = mo_inc_total - mo_exp_total

    st.markdown(f"""
    <div class="cal-header">
        <div style="font-size:1.2em; font-weight:900; color:white">
            {calendar.month_name[cal_month]} {cal_year}
        </div>
        <div style="display:flex; justify-content:center; gap:24px; margin-top:10px">
            <div>
                <div style="font-size:1.3em; font-weight:900; color:#a8ffd4">
                    {SYMBOL}{mo_inc_total:,.0f}
                </div>
                <div style="font-size:0.75em; opacity:0.8; color:white">Income</div>
            </div>
            <div>
                <div style="font-size:1.3em; font-weight:900; color:#ffb3d4">
                    {SYMBOL}{mo_exp_total:,.0f}
                </div>
                <div style="font-size:0.75em; opacity:0.8; color:white">Expense</div>
            </div>
            <div>
                <div style="font-size:1.3em; font-weight:900; color:white">
                    {SYMBOL}{mo_bal:,.0f}
                </div>
                <div style="font-size:0.75em; opacity:0.8; color:white">Balance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    daily_exp = {}
    daily_inc = {}
    for e in mo_exp:
        d = int(e["date"].split("-")[2])
        daily_exp[d] = daily_exp.get(d, 0) + e["amount"]
    for e in mo_inc:
        d = int(e["date"].split("-")[2])
        daily_inc[d] = daily_inc.get(d, 0) + e["amount"]

    day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    hcols = st.columns(7)
    for i, dn in enumerate(day_names):
        hcols[i].markdown(
            f"<div style='text-align:center; font-weight:800; color:#00897b;"
            f"font-size:0.78em; padding:4px'>{dn}</div>",
            unsafe_allow_html=True)

    for week in calendar.monthcalendar(cal_year, cal_month):
        wcols = st.columns(7)
        for i, day in enumerate(week):
            with wcols[i]:
                if day == 0:
                    st.markdown("<div style='min-height:58px'></div>",
                               unsafe_allow_html=True)
                else:
                    exp_amt = daily_exp.get(day, 0)
                    inc_amt = daily_inc.get(day, 0)
                    is_today = (day == today.day and
                                cal_month == today.month and
                                cal_year == today.year)
                    if is_today:
                        bg = "linear-gradient(135deg,#00b894,#00897b)"
                        tc = "white"
                    elif exp_amt > 0:
                        alpha = min(0.15 + exp_amt / 200 * 0.5, 0.7)
                        bg    = f"rgba(0,184,148,{alpha})"
                        tc    = "#333"
                    else:
                        bg = "white"
                        tc = "#333"

                    exp_txt = (f"<div style='color:{'white' if is_today else '#00b894'};"
                               f"font-size:0.65em;font-weight:700'>{SYMBOL}{exp_amt:.0f}</div>"
                               if exp_amt > 0 else "")
                    inc_txt = (f"<div style='color:{'white' if is_today else '#2ecc71'};"
                               f"font-size:0.65em;font-weight:700'>+{SYMBOL}{inc_amt:.0f}</div>"
                               if inc_amt > 0 else "")

                    st.markdown(f"""
                    <div style="background:{bg}; border-radius:10px; padding:5px 3px;
                                text-align:center; min-height:58px; margin:2px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.05)">
                        <div style="font-weight:800; color:{tc}; font-size:0.9em">{day}</div>
                        {exp_txt}{inc_txt}
                    </div>
                    """, unsafe_allow_html=True)

    if mo_exp:
        st.markdown('<div class="section-title">📋 This Month</div>',
                   unsafe_allow_html=True)
        by_date = {}
        for e in sorted(mo_exp, key=lambda x: x["date"], reverse=True):
            by_date.setdefault(e["date"], []).append(e)

        for d, txs in list(sorted(by_date.items(), reverse=True))[:5]:
            dt        = datetime.strptime(d, "%Y-%m-%d")
            dow       = dt.strftime("%A")
            day_total = sum(t["amount"] for t in txs)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between;
                        align-items:center; margin:12px 0 6px 0">
                <span style="font-family:'Dancing Script',cursive;
                             font-size:1.1em; color:#00897b">
                    {dow}, {dt.strftime('%b %d')}
                </span>
                <span style="color:#00b894; font-weight:700">
                    OUT {SYMBOL}{day_total:.0f}
                </span>
            </div>
            """, unsafe_allow_html=True)
            for tx in txs:
                icon  = CAT_ICONS.get(tx["category"], "✨")
                color = CAT_COLORS.get(tx["category"], "#eee")
                st.markdown(f"""
                <div class="tx-row">
                    <div style="display:flex; align-items:center; gap:10px">
                        <div style="background:{color}; border-radius:10px;
                                    width:34px; height:34px; display:flex;
                                    align-items:center; justify-content:center">
                            {icon}
                        </div>
                        <div>
                            <div style="font-weight:700; font-size:0.9em; color:#333">
                                {tx['description']}
                            </div>
                            <div style="color:#aaa; font-size:0.75em">{tx['category']}</div>
                        </div>
                    </div>
                    <div class="tx-expense">{SYMBOL}{tx['amount']:.2f}</div>
                </div>
                """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 4 — CHARTS
# ════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">📊 Insights</div>', unsafe_allow_html=True)

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)

        ct = df.groupby("category")["amount"].sum().reset_index()
        ct["label"] = ct["category"].map(CAT_ICONS) + " " + ct["category"]
        fig1 = px.pie(ct, values="amount", names="label",
                     title="🌸 Where did my money go?",
                     color_discrete_sequence=GREEN, hole=0.45)
        fig1.update_traces(textposition='outside', textinfo='percent+label')
        fig1.update_layout(font_family="Nunito", showlegend=False,
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          title_font_color="#00897b")
        st.plotly_chart(fig1, use_container_width=True)

        dd = df.groupby("date")["amount"].sum().reset_index()
        fig2 = px.area(dd, x="date", y="amount",
                      title="📅 Daily Spending Trend",
                      color_discrete_sequence=["#00b894"])
        fig2.update_traces(fill='tozeroy',
                          fillcolor='rgba(0,184,148,0.15)',
                          line_color="#00b894")
        fig2.update_layout(font_family="Nunito",
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          title_font_color="#00897b")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name=f"💵 Income", x=["This Month"],
                             y=[st.session_state.monthly_income],
                             marker_color="#00897b", marker_line_width=0))
        fig3.add_trace(go.Bar(name=f"💸 Spent", x=["This Month"],
                             y=[total_spent()],
                             marker_color="#00b894", marker_line_width=0))
        fig3.update_layout(title="💰 Income vs Spending", barmode="group",
                          font_family="Nunito",
                          plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          title_font_color="#00897b")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.markdown("""
        <div style="background:white; border-radius:20px; padding:40px;
                    text-align:center; box-shadow:0 4px 15px rgba(0,184,148,0.1)">
            <div style="font-size:3em">📊</div>
            <div style="color:#00897b; font-weight:700; margin-top:10px">
                Add expenses to see insights! ✨
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 5 — BUDGET
# ════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🎯 Budget Planner</div>',
               unsafe_allow_html=True)

    cs            = cat_spending()
    total_budget  = sum(st.session_state.budgets.values())
    total_spent_n = total_spent()
    budget_pct    = (total_spent_n / total_budget * 100) if total_budget > 0 else 0

    if total_budget > 0:
        fig_donut = go.Figure(go.Pie(
            values=[total_spent_n, max(total_budget - total_spent_n, 0)],
            labels=["Spent","Remaining"],
            hole=0.65,
            marker_colors=["#00b894","#e0f7f4"],
            textinfo="none"
        ))
        fig_donut.update_layout(
            showlegend=False, margin=dict(t=0,b=0,l=0,r=0),
            height=200,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(
                text=f"<b>{budget_pct:.0f}%</b><br>used",
                x=0.5, y=0.5, font_size=18,
                font_color="#00897b", showarrow=False
            )]
        )
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown(f"""
        <div style="text-align:center; color:#00b894; font-size:1.1em;
                    font-weight:800; margin:-15px 0 15px">
            {SYMBOL}{total_spent_n:.0f} / {SYMBOL}{total_budget:.0f}
        </div>
        """, unsafe_allow_html=True)

    with st.form("budget_form"):
        for cat in CATEGORIES:
            icon  = CAT_ICONS[cat]
            color = CAT_COLORS[cat]
            sp    = cs.get(cat, 0)
            lim   = st.session_state.budgets.get(cat, 0.0)
            pct   = (sp / lim * 100) if lim > 0 else 0
            bar_c = "#00b894" if pct > 100 else "#ff9800" if pct > 80 else "#2ecc71"

            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:8px; margin:8px 0">
                    <div style="background:{color}; border-radius:10px;
                                width:32px; height:32px; display:flex;
                                align-items:center; justify-content:center">{icon}</div>
                    <div>
                        <div style="font-weight:700; font-size:0.85em; color:#333">
                            {cat.split(' & ')[0]}
                        </div>
                        <div style="color:{bar_c}; font-size:0.75em; font-weight:700">
                            {SYMBOL}{sp:.0f}{' / '+SYMBOL+str(int(lim)) if lim > 0 else ''}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if lim > 0:
                    st.progress(min(pct / 100, 1.0))
            with col3:
                st.session_state.budgets[cat] = st.number_input(
                    f"Limit ({SYMBOL})", min_value=0.0, value=lim,
                    step=10.0, key=f"bgt_{cat}",
                    label_visibility="collapsed")

        if st.form_submit_button("💾 Save Budgets ✨", use_container_width=True):
            st.success("🌸 Budgets saved!")
            st.rerun()

# ════════════════════════════════════════
# TAB 6 — GOALS
# ════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">🌟 Savings Goals</div>',
               unsafe_allow_html=True)
    st.markdown("Dream it. Save it. Get it! 💜")

    with st.form("goal_form"):
        col1, col2 = st.columns(2)
        with col1:
            gname   = st.text_input("🎯 Goal", placeholder="New phone, Vacation...")
            gtarget = st.number_input(f"💵 Target ({SYMBOL})", min_value=1.0, step=10.0)
        with col2:
            gsaved    = st.number_input(f"💰 Saved so far ({SYMBOL})", min_value=0.0, step=10.0)
            gdeadline = st.date_input("📅 By when?")
            gemoji    = st.text_input("🎨 Emoji", value="🌸", max_chars=2)

        if st.form_submit_button("Add Goal 🌟", use_container_width=True):
            if gname and gtarget > 0:
                st.session_state.goals.append({
                    "name":gname, "target":gtarget,
                    "saved":gsaved, "deadline":str(gdeadline),
                    "emoji":gemoji
                })
                st.success(f"🌸 Added: {gname}")
                st.rerun()

    if st.session_state.goals:
        for i, g in enumerate(st.session_state.goals):
            pct  = min(g["saved"] / g["target"] * 100, 100)
            rem  = g["target"] - g["saved"]
            due  = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
            dl   = (due - date.today()).days
            done = pct >= 100

            st.markdown(f"""
            <div class="goal-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start">
                    <div>
                        <span style="font-size:2em">{g.get('emoji','🌸')}</span>
                        <strong style="font-size:1.1em; color:#333; margin-left:8px">
                            {g['name']}
                        </strong>
                        {'<span style="color:#00b894; margin-left:6px">🎉 Done!</span>'
                         if done else ''}
                    </div>
                    <div style="text-align:right">
                        <div style="color:#00b894; font-size:1.3em; font-weight:900">
                            {SYMBOL}{g['saved']:,.0f}
                        </div>
                        <div style="color:#aaa; font-size:0.8em">of {SYMBOL}{g['target']:,.0f}</div>
                    </div>
                </div>
                <div style="margin:10px 0 4px; color:#888; font-size:0.82em; font-weight:700">
                    📅 {dl} days left · 💰 {SYMBOL}{rem:,.0f} to go · {pct:.0f}% complete
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(pct / 100)

            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                add_amt = st.number_input(f"Add {SYMBOL}", min_value=0.01, step=10.0,
                                          key=f"gadd_{i}",
                                          label_visibility="collapsed",
                                          placeholder="Add amount...")
            with col2:
                if st.button("➕ Add Money", key=f"gsave_{i}"):
                    st.session_state.goals[i]["saved"] += add_amt
                    st.success(f"🌸 Added {SYMBOL}{add_amt:.0f} to {g['name']}!")
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"gdel_{i}"):
                    st.session_state.goals.pop(i)
                    st.rerun()

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("🌟 Goals", len(st.session_state.goals))
        c2.metric("🎯 Target",
                 f"{SYMBOL}{sum(g['target'] for g in st.session_state.goals):,.0f}")
        c3.metric("💰 Saved",
                 f"{SYMBOL}{sum(g['saved'] for g in st.session_state.goals):,.0f}")
    else:
        st.markdown("""
        <div style="background:white; border-radius:20px; padding:35px;
                    text-align:center; box-shadow:0 4px 15px rgba(0,184,148,0.1)">
            <div style="font-size:2.5em">🌟</div>
            <div style="color:#00897b; font-weight:700; margin-top:10px">
                No goals yet! Set your first savings goal ✨
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════
# TAB 7 — AI ADVISOR
# ════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-title">🤖 AI Money Advisor</div>',
               unsafe_allow_html=True)
    st.markdown("Ask me anything about your finances! 💜")

    spent   = total_spent()
    balance = st.session_state.monthly_income - spent
    cs      = cat_spending()
    breakdown = "\n".join([f"- {k}: {SYMBOL}{v:.2f}" for k, v in cs.items()]) \
                or "No expenses yet."

    context = f"""
Monthly Income: {SYMBOL}{st.session_state.monthly_income:.2f}
Total Spent: {SYMBOL}{spent:.2f}
Remaining Balance: {SYMBOL}{balance:.2f}
Currency: {st.session_state.currency}
Spending Breakdown:
{breakdown}
Savings Goals: {len(st.session_state.goals)} goals,
total saved {SYMBOL}{sum(g['saved'] for g in st.session_state.goals):.2f}
"""
    system = SystemMessage(content=f"""You are a friendly, cute and smart personal
financial advisor named Penny 🌸. You have access to the user's real financial data:
{context}
Give personalized, specific advice using their actual numbers.
Be encouraging, supportive and use cute emojis. Keep responses clear and concise.""")

    st.markdown("**💬 Quick Questions:**")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("💸 Overspending?"):
            st.session_state.chat_history.append(
                HumanMessage(content="Where am I overspending?"))
    with q2:
        if st.button("💰 How much save?"):
            st.session_state.chat_history.append(
                HumanMessage(content="How much can I save this month?"))
    with q3:
        if st.button("✨ Saving tips"):
            st.session_state.chat_history.append(
                HumanMessage(content="Give me 5 cute saving tips based on my spending!"))

    st.markdown("---")

    if not st.session_state.chat_history:
        st.markdown("""
        <div style="background:white; border-radius:20px; padding:20px;
                    box-shadow:0 4px 15px rgba(0,184,148,0.1);
                    border-left:4px solid #00b894; margin-bottom:10px">
            <div style="display:flex; align-items:center; gap:10px">
                <span style="font-size:1.8em">🌸</span>
                <div>
                    <div style="font-weight:700; color:#333">Penny — AI Advisor</div>
                    <div style="color:#888; font-size:0.9em">
                        Hi! I'm Penny, your personal finance advisor 🌸
                        I can see your income and expenses.
                        Ask me anything about your money! 💜
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            st.chat_message("user", avatar="🧑").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant", avatar="🌸").write(msg.content)

    if (st.session_state.chat_history and
            isinstance(st.session_state.chat_history[-1], HumanMessage)):
        if len(st.session_state.chat_history) == 1 or \
           not isinstance(st.session_state.chat_history[-2], HumanMessage):
            with st.spinner("Penny is thinking... 🌸"):
                resp = st.session_state.llm.invoke(
                    [system] + st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=resp.content))
            st.rerun()

    if user_input := st.chat_input("Ask Penny about your finances... 💜"):
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.chat_message("user", avatar="🧑").write(user_input)
        with st.spinner("Penny is thinking... 🌸"):
            resp = st.session_state.llm.invoke(
                [system] + st.session_state.chat_history)
        st.session_state.chat_history.append(AIMessage(content=resp.content))
        st.chat_message("assistant", avatar="🌸").write(resp.content)

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()