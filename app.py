import streamlit as st
import pandas as pd

st.set_page_config(page_title="TIN Verification", layout="centered")

st.title("🔍 TIN ডাটাবেজ সার্চ")
st.write("১২ ডিজিটের TIN নম্বরটি দিয়ে সার্চ করুন।")

@st.cache_data
def load_data():
    # নিশ্চিত করুন ফাইলের নাম tin_data.csv
    return pd.read_csv("tin_data.csv", encoding="utf-8")

try:
    df = load_data()
    search_query = st.text_input("TIN নম্বর লিখুন:", placeholder="যেমন: 123456789012")

    if st.button("সার্চ করুন"):
        if search_query:
            # সার্চ লজিক
            result = df[df['TIN'].astype(str) == str(search_query).strip()]
            
            if not result.empty:
                st.success("তথ্য পাওয়া গেছে!")
                for _, row in result.iterrows():
                    st.markdown(f"""
                    <div style="padding:15px; border-radius:10px; background-color:#f0f2f6; border-left:5px solid #1f4e78; margin-bottom:10px;">
                        <p><b>নাম:</b> {row['NAME']}</p>
                        <p><b>TIN:</b> {row['TIN']}</p>
                        <p><b>ঠিকানা:</b> {row['Address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("দুঃখিত, এই TIN নম্বরের কোনো তথ্য পাওয়া যায়নি।")
except Exception as e:
    st.error("আপনার CSV ফাইলটি (tin_data.csv) খুঁজে পাওয়া যায়নি।")