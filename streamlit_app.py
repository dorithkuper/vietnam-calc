import streamlit as st
import requests

st.set_page_config(page_title="מחשבון מטבע וייטנאם", page_icon="🇻🇳")
st.title("מחשבון מטבע מתעדכן בזמן אמת 💹")

# פונקציה למשיכת שערים מהרשת
def get_live_rates():
    try:
        # API חינמי (מעדכן פעם ביום בגרסה החינמית)
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()
        
        usd_to_vnd = data['rates']['VND']
        usd_to_ils = data['rates']['ILS']
        
        # חישוב שקל לדונג דרך הדולר
        ils_to_vnd = usd_to_vnd / usd_to_ils
        
        return ils_to_vnd, usd_to_vnd, True
    except:
        # שערי גיבוי במקרה שאין אינטרנט
        return 6850.0, 25200.0, False

# משיכת הנתונים
ils_to_vnd_rate, usd_to_vnd_rate, is_live = get_live_rates()

# הצגת סטטוס העדכון
if is_live:
    st.caption(f"✅ שערים מעודכנים בזמן אמת מהרשת")
else:
    st.caption("⚠️ מצב אופליין: משתמש בשערי ברירת מחדל")

# ממשק המשתמש
st.divider()

col1, col2 = st.columns(2)
with col1:
    option = st.selectbox("מטבע מקור:", ["שקל (ILS)", "דולר (USD)", "דונג (VND)"])
with col2:
    amount = st.number_input("סכום להמרה:", min_value=0.0, value=1.0, step=1.0)

st.divider()

# לוגיקת החישוב
if option == "שקל (ILS)":
    vnd = amount * ils_to_vnd_rate
    usd = amount * (usd_to_vnd_rate / ils_to_vnd_rate) / (usd_to_vnd_rate / (usd_to_vnd_rate / (usd_to_vnd_rate/usd_to_vnd_rate))) # פשטתי את הלוגיקה למטה
    # חישוב נקי
    usd = amount / (usd_to_vnd_rate / ils_to_vnd_rate) 
    
    st.metric("בווייטנאמי (VND)", f"{vnd:,.0f} ₫")
    st.metric("בדולר (USD)", f"${amount / (usd_to_vnd_rate / ils_to_vnd_rate):.2f}")

elif option == "דונג (VND)":
    ils = amount / ils_to_vnd_rate
    usd = amount / usd_to_vnd_rate
    st.metric("בשקלים (ILS)", f"₪{ils:.2f}")
    st.metric("בדולר (USD)", f"${usd:.2f}")

elif option == "דולר (USD)":
    vnd = amount * usd_to_vnd_rate
    ils = amount * (usd_to_vnd_rate / ils_to_vnd_rate)
    st.metric("בווייטנאמי (VND)", f"{vnd:,.0f} ₫")
    st.metric("בשקלים (ILS)", f"₪{amount * (usd_to_vnd_rate / ils_to_vnd_rate):.2f}")

# הצגת שערי ההמרה ששימשו לחישוב (לביקורת)
with st.expander("ראה שערי חליפין נוכחיים"):
    st.write(f"1 ₪ = {ils_to_vnd_rate:,.2f} VND")
    st.write(f"1 $ = {usd_to_vnd_rate:,.2f} VND")
