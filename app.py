from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# ১. ডাটা লোড করা (ফাইলটি app.py এর একই ফোল্ডারে রাখুন)
# আপনার বড় ফাইলের নাম এখানে দিন অথবা ফাইলটি রিনেম করে 'audit_data.csv' দিন
FILE_NAME = 'AUDIT_SELECTION_2023-24.xlsx - AUDIT_SELECTION_23-24_DETAILS.csv'

def load_data():
    if os.path.exists(FILE_NAME):
        # dtype={'tin': str} ব্যবহার করা হয়েছে যাতে বড় নম্বর বৈজ্ঞানিক ফরম্যাটে (4.57E+11) না চলে যায়
        df = pd.read_csv(FILE_NAME, dtype={'tin': str})
        # সার্চ দ্রুত করার জন্য TIN নম্বরকে ইন্ডেক্স হিসেবে সেট করা হলো
        df.set_index('tin', inplace=False)
        return df
    return None

df = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if df is None:
        return "Error: ডাটা ফাইল পাওয়া যায়নি!"

    # ইউজারের ইনপুট নেয়া এবং বাড়তি স্পেস বাদ দেয়া
    search_tin = request.form.get('tin_number', '').strip()

    if not search_tin:
        return "অনুগ্রহ করে একটি TIN নম্বর দিন।"

    # ডাটাফ্রেমে সার্চ করা
    # যেহেতু ডাটা অনেক বেশি, তাই .loc ব্যবহার করা দ্রুততর
    result = df[df['tin'] == search_tin]

    if not result.empty:
        # রেজাল্ট পাওয়া গেলে তা ডিকশনারি আকারে টেমপ্লেটে পাঠানো
        data = result.to_dict(orient='records')[0]
        return render_template('result.html', data=data)
    else:
        return render_template('result.html', error="দুঃখিত, এই TIN নম্বরটি অডিট তালিকায় পাওয়া যায়নি।")

if __name__ == '__main__':
    app.run(debug=True)
