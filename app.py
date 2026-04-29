import streamlit as st
import pandas as pd
import os

# ফাইলের নাম ঠিক করে নিন
FILE_NAME = "tin_data.xlsx" # যদি আপনার ফাইলটি CSV হয় তবে এখানে "tin_data.csv" লিখুন

st.set_page_config(page_title="TIN Search Portal", layout="centered")

@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        # ফাইল ফরম্যাট অনুযায়ী নিচের লাইনটি কাজ করবে
        if FILE_NAME.endswith('.xlsx'):
            return pd.read_excel(FILE_NAME)
        else:
            return pd.read_csv(FILE_NAME)
    else:
        return None

df = load_data()

if df is None:
    st.error(f"❌ আপনার ফাইলটি পাওয়া যায়নি! নিশ্চিত করুন যে ফাইলের নাম হুবহু '{FILE_NAME}' এবং এটি আপনার কোডের সাথেই আপলোড করা হয়েছে।")
else:
    st.success("✅ ডাটাবেজ কানেক্টেড!")
    # বাকি সার্চ কোড এখানে...
    search_input = st.text_input("TIN নম্বর দিন:")
    if st.button("সার্চ"):
        result = df[df['TIN'].astype(str) == search_input]
        if not result.empty:
            st.write(result)
        else:
            st.warning("তথ্য পাওয়া যায়নি।")
