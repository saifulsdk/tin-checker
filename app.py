import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBRAudit - TIN Search Tool", layout="wide")

st.title("🔍 TIN Data Audit & Search")
st.write("Search the Taxpayer Identification Number database.")

@st.cache_data
def load_data():
    file_path = "tin_data.csv"
    try:
        # Attempt to load as CSV with fallback encoding
        return pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding='latin1')
    except Exception:
        # If it's actually an Excel file renamed to .csv
        return pd.read_excel(file_path)

# Load the data
try:
    df = load_data()
    
    # Search Bars
    col1, col2 = st.columns(2)
    with col1:
        search_tin = st.text_input("Search by TIN Number")
    with col2:
        search_name = st.text_input("Search by Name")

    # Filter Logic
    filtered_df = df.copy()
    if search_tin:
        filtered_df = filtered_df[filtered_df.iloc[:, 0].astype(str).str.contains(search_tin, case=False)]
    if search_name:
        filtered_df = filtered_df[filtered_df.iloc[:, 1].astype(str).str.contains(search_name, case=False)]

    # Display Results
    st.subheader(f"Results ({len(filtered_df)} found)")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load data. The file 'tin_data.csv' might be corrupted or in a binary format. Error: {e}")
    st.info("Tip: Try opening the file in Excel and 'Saving As' a proper CSV (Comma Delimited) file.")
