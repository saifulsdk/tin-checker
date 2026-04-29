import streamlit as st
import pandas as pd

# ওয়েবসাইটের টাইটেল এবং কনফিগারেশন
st.set_page_config(page_title="TIN Data Audit Tool", layout="wide")
st.title("🔍 TIN Data Lookup System")

# ডাটা লোড করার ফাংশন
@st.cache_data
def load_data():
    # আপনার আপলোড করা ফাইলের নাম এখানে নিশ্চিত করুন
    df = pd.read_csv("tin_data.csv")
    return df

try:
    df = load_data()

    # সার্চ বার তৈরি
    search_term = st.text_input("TIN নম্বর বা নাম দিয়ে সার্চ করুন:", "")

    if search_term:
        # ডাটা সার্চ লজিক (সবগুলো কলামে সার্চ করবে)
        results = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        
        if not results.empty:
            st.success(f"{len(results)}টি তথ্য পাওয়া গেছে।")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("কোনো তথ্য খুঁজে পাওয়া যায়নি।")
    else:
        st.info("সার্চ করার জন্য উপরে বক্স-এ লিখুন।")
        # প্রথম কিছু ডাটা প্রদর্শন
        st.write("ডেটা প্রিভিউ:")
        st.secondary_data = df.head(10)
        st.table(st.secondary_data)

except Exception as e:
    st.error(f"Error: {e}")
