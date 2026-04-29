import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Audit Selection Checker", layout="centered")

st.title("🔍 অডিট সিলেকশন চেক করুন (২০২৩-২৪)")

# ডাটা ফাইল লোড করা
FILE_NAME = 'AUDIT_SELECTION_2023-24.xlsx - AUDIT_SELECTION_23-24_DETAILS.csv'

@st.cache_data # এতে বারবার ফাইল লোড হবে না, অ্যাপ ফাস্ট থাকবে
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME, dtype={'tin': str})
    return None

df = load_data()

if df is not None:
    tin_input = st.text_input("আপনার ১২ ডিজিটের TIN নম্বরটি লিখুন:", placeholder="e.g. 782291231739")

    if st.button("সার্চ করুন"):
        if tin_input:
            # সার্চ করা
            result = df[df['tin'] == tin_input.strip()]
            
            if not result.empty:
                st.success("✅ অভিনন্দন! আপনার টিআইএন অডিট তালিকায় পাওয়া গেছে।")
                
                # সুন্দরভাবে তথ্য দেখানো
                res = result.iloc[0]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**TIN:** {res['tin']}")
                    st.write(f"**ট্যাক্স জোন:** {res['zone']}")
                with col2:
                    st.write(f"**সার্কেল:** {res['circle']}")
                    st.write(f"**অ্যাসেসমেন্ট ইয়ার:** {res['assessment_year']}")
            else:
                st.error("❌ দুঃখিত, এই TIN নম্বরটি অডিট তালিকায় নেই।")
        else:
            st.warning("অনুগ্রহ করে একটি TIN নম্বর দিন।")
else:
    st.error("ডাটা ফাইল (CSV) খুঁজে পাওয়া যায়নি। দয়া করে নিশ্চিত করুন ফাইলটি আপলোড করা হয়েছে।")
