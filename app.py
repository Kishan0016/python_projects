import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from pathlib import Path

st.set_page_config(page_title='Expense Tracker', page_icon='💰', layout='wide')

# Change these colors to customize the UI
PRIMARY_COLOR = '#2563EB'
INCOME_COLOR = '#16A34A'
EXPENSE_COLOR = '#DC2626'
BALANCE_COLOR = '#7C3AED'
CARD_BG = "#43B6F0"
TEXT_COLOR = "#E2BABA"
MUTED_COLOR = '#64748B'
BORDER_COLOR = '#E2E8F0'
DATA_FILE = Path('expenses.csv')
COLUMNS = ['Date','Type','Category','Description','Amount','Payment Method']

st.markdown(f'''<style>
.main-title {{font-size:42px;font-weight:700;color:{TEXT_COLOR};margin-bottom:0;}}
.subtitle {{color:{MUTED_COLOR};font-size:17px;margin-bottom:25px;}}
.metric-card {{background:{CARD_BG};border:1px solid {BORDER_COLOR};border-radius:14px;padding:20px;min-height:120px;}}
.metric-title {{color:{MUTED_COLOR};font-size:15px;margin-bottom:8px;}}
.metric-value {{font-size:28px;font-weight:700;}}
.income-value {{color:{INCOME_COLOR};}} .expense-value {{color:{EXPENSE_COLOR};}} .balance-value {{color:{BALANCE_COLOR};}}
div.stButton > button {{border-radius:8px;font-weight:600;}}
</style>''', unsafe_allow_html=True)

def load_data():
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
                df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
                df = df.dropna(subset=['Date','Amount'])
                for col in COLUMNS:
                    if col not in df.columns: df[col] = ''
                return df[COLUMNS]
        except Exception:
            st.warning('Could not read existing data. Starting with an empty tracker.')
    return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_transaction(transaction_date, transaction_type, category, description, amount, payment_method):
    new_row = pd.DataFrame([{'Date':transaction_date,'Type':transaction_type,'Category':category,'Description':description,'Amount':amount,'Payment Method':payment_method}])
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
    save_data(st.session_state.data)

if 'data' not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data.copy()
total_income = df.loc[df['Type']=='Income','Amount'].sum() if not df.empty else 0
total_expense = df.loc[df['Type']=='Expense','Amount'].sum() if not df.empty else 0
balance = total_income - total_expense

st.sidebar.title('💰 Expense Tracker')
page = st.sidebar.radio('Navigation', ['📊 Dashboard','➕ Add Transaction','📋 Transactions','📈 Analytics'])
st.sidebar.divider()
st.sidebar.info('Track income and expenses, analyze spending patterns, and manage your budget.')

if page == '📊 Dashboard':
    st.markdown('<div class="main-title">💰 Expense Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Personal finance dashboard</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    cards = [(c1,'💵 Total Income',total_income,'income-value'),(c2,'💸 Total Expenses',total_expense,'expense-value'),(c3,'💰 Current Balance',balance,'balance-value'),(c4,'🧾 Transactions',len(df),'')]
    for col,label,value,cls in cards:
        with col:
            display = f'₹{value:,.2f}' if label != '🧾 Transactions' else str(value)
            st.markdown(f'<div class="metric-card"><div class="metric-title">{label}</div><div class="metric-value {cls}">{display}</div></div>', unsafe_allow_html=True)
    st.write('')
    if df.empty:
        st.info("No transactions yet. Go to 'Add Transaction' to get started.")
    else:
        c1,c2 = st.columns(2)
        with c1:
            st.subheader('📊 Expenses by Category')
            e = df[df['Type']=='Expense']
            if not e.empty:
                cat = e.groupby('Category',as_index=False)['Amount'].sum().sort_values('Amount',ascending=False)
                st.plotly_chart(px.pie(cat,names='Category',values='Amount',hole=.45),use_container_width=True)
            else: st.info('No expense data available.')
        with c2:
            st.subheader('💵 Income vs Expense')
            comp = pd.DataFrame({'Type':['Income','Expense'],'Amount':[total_income,total_expense]})
            st.plotly_chart(px.bar(comp,x='Type',y='Amount',text_auto='.2f'),use_container_width=True)
        st.subheader('🕒 Recent Transactions')
        st.dataframe(df.sort_values('Date',ascending=False).head(5),use_container_width=True,hide_index=True)

elif page == '➕ Add Transaction':
    st.title('➕ Add Transaction')
    with st.form('transaction_form'):
        c1,c2 = st.columns(2)
        with c1:
            transaction_date = st.date_input('Date',value=date.today())
            transaction_type = st.selectbox('Transaction Type',['Expense','Income'])
            category = st.selectbox('Category',['Food','Travel','Shopping','Bills','Entertainment','Health','Education','Rent','Salary','Investment','Other'])
        with c2:
            description = st.text_input('Description',placeholder='e.g. Grocery shopping')
            amount = st.number_input('Amount (₹)',min_value=0.01,step=100.0,format='%.2f')
            payment_method = st.selectbox('Payment Method',['Cash','UPI','Debit Card','Credit Card','Bank Transfer'])
        submitted = st.form_submit_button('💾 Save Transaction',use_container_width=True)
    if submitted:
        if not description.strip(): st.error('Please enter a transaction description.')
        elif amount <= 0: st.error('Please enter a valid amount.')
        else:
            add_transaction(transaction_date,transaction_type,category,description.strip(),amount,payment_method)
            st.success(f'✅ {transaction_type} of ₹{amount:,.2f} added successfully!')

elif page == '📋 Transactions':
    st.title('📋 Transactions')
    if df.empty: st.info('No transactions available.')
    else:
        c1,c2,c3 = st.columns(3)
        with c1: type_filter = st.selectbox('Type',['All','Income','Expense'])
        with c2: category_filter = st.selectbox('Category',['All']+sorted(df['Category'].dropna().unique().tolist()))
        with c3: search = st.text_input('Search',placeholder='Search description...')
        filtered = df.copy()
        if type_filter != 'All': filtered = filtered[filtered['Type']==type_filter]
        if category_filter != 'All': filtered = filtered[filtered['Category']==category_filter]
        if search: filtered = filtered[filtered['Description'].astype(str).str.contains(search,case=False,na=False)]
        st.write(f'Showing **{len(filtered)}** transaction(s)')
        st.dataframe(filtered.sort_values('Date',ascending=False),use_container_width=True,hide_index=True)
        st.divider(); st.subheader('🗑️ Delete Transaction')
        options = {}
        for index,row in df.iterrows():
            label = f"{index} | {row['Date']} | {row['Type']} | {row['Category']} | ₹{row['Amount']:,.2f} | {row['Description']}"
            options[label] = index
        selected = st.selectbox('Select transaction to delete',list(options.keys()))
        if st.button('🗑️ Delete Selected Transaction'):
            idx = options[selected]
            st.session_state.data = st.session_state.data.drop(index=idx).reset_index(drop=True)
            save_data(st.session_state.data); st.success('Transaction deleted successfully.'); st.rerun()

else:
    st.title('📈 Expense Analytics')
    if df.empty: st.info('Add some transactions to view analytics.')
    else:
        expense_df = df[df['Type']=='Expense'].copy()
        if expense_df.empty: st.info('Add expense transactions to view spending analytics.')
        else:
            cat = expense_df.groupby('Category',as_index=False)['Amount'].sum().sort_values('Amount',ascending=False)
            st.subheader('🏷️ Category-wise Spending')
            st.plotly_chart(px.bar(cat,x='Category',y='Amount',text_auto='.2f'),use_container_width=True)
            expense_df['Month'] = pd.to_datetime(expense_df['Date']).dt.strftime('%Y-%m')
            monthly = expense_df.groupby('Month',as_index=False)['Amount'].sum()
            st.subheader('📅 Monthly Expenses')
            st.plotly_chart(px.line(monthly,x='Month',y='Amount',markers=True),use_container_width=True)
            payment = expense_df.groupby('Payment Method',as_index=False)['Amount'].sum().sort_values('Amount',ascending=False)
            st.subheader('💳 Spending by Payment Method')
            st.plotly_chart(px.bar(payment,x='Payment Method',y='Amount',text_auto='.2f'),use_container_width=True)

st.divider(); st.caption('💰 Expense Tracker | Built with Python, Pandas, Plotly & Streamlit')
