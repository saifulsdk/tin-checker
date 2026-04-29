import streamlit as st
import pandas as pd
import os

# পেজ সেটআপ
st.set_page_config(page_title="Audit Selection Checker", layout="centered")

st.title("🔍 অডিট সিলেকশন চেক করুন (২০২৩-২৪)")

# আপনার ফাইলের নাম
FILE_NAME = 'audit_data.xlsx'

@st.cache_data
def load_data():
    if os.path.exists(FILE_NAME):
        try:
            # Excel ফাইল পড়ার জন্য engine='openpyxl' ব্যবহার করা হয়েছে
            data = pd.read_excel(FILE_NAME, dtype={'tin': str}, engine='openpyxl')
            return data
        except Exception as e:
            st.error(f"ফাইলটি পড়তে সমস্যা হচ্ছে: {e}")
            return None
    return None

df = load_data()

if df is not None:
    # ইউজার ইন্টারফেস
    tin_input = st.text_input("আপনার ১২ ডিজিটের TIN নম্বরটি লিখুন:", placeholder="যেমন: 782291231739")

    if st.button("সার্চ করুন"):
        if tin_input:
            clean_tin = tin_input.strip()
            # ডাটাফ্রেমে সার্চ
            result = df[df['tin'] == clean_tin]
            
            if not result.empty:
                # আপনার সংশোধিত মেসেজটি এখানে যুক্ত করা হয়েছে
                st.error("⚠️ আপনার টিআইএন অডিট তালিকায় পাওয়া গেছে। অতি স্বত্বর আপনার একজন কর আইনজীবী বা স্থানীয় কর কমিশনার অফিসে যোগাযোগ করুন।")
                
                res = result.iloc[0]
                
                # তথ্যগুলো কার্ড আকারে প্রদর্শন
                st.markdown("---")
                st.subheader("📋 অডিট ডিটেইলস:")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**TIN নম্বর:**\n{res['tin']}")
                    st.info(f"**ট্যাক্স জোন:**\n{res['zone']}")
                with col2:
                    st.info(f"**সার্কেল:**\n{res['circle']}")
                    st.info(f"**কর বর্ষ:**\n{res['assessment_year']}")
            else:
                # তালিকায় না থাকলে এই মেসেজটি দেখাবে
                st.success("✅ এই TIN নম্বরটি অডিট তালিকায় পাওয়া যায়নি।")
        else:
            st.warning("অনুগ্রহ করে একটি TIN নম্বর টাইপ করুন।")
else:
    st.error(f"'{FILE_NAME}' ফাইলটি পাওয়া যায়নি।")
    st.info("আপনার GitHub-এ 'audit_data.xlsx' ফাইলটি আপলোড করা হয়েছে কি না নিশ্চিত করুন।")
