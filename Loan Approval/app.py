import streamlit as st
import pandas as pd
import pickle as pk

# Load Model and Scaler
model = pk.load(open('model.pkl', 'rb'))
scaler = pk.load(open('scaler.pkl', 'rb'))

# Apply Custom CSS for a Stunning UI
st.markdown("""
    <style>
        /* Background Styling */
        .stApp {
            background: #2f2f2f;  /* Solid grey background */
            color: white;
        }

        /* Header Styling */
        .st-emotion-cache-1d391kg {
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            padding: 20px;
            text-align: center;
            border-radius: 15px;
            font-size: 36px;
            font-weight: bold;
            color: white;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        }

        /* Section Styling */
        .section-box {
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 15px;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0px 5px 10px rgba(0,0,0,0.2);
        }

        /* Custom Labels */
        .education { color: #FFD700; }
        .employment { color: #1E90FF; }
        .income { color: #FF4500; }
        .loan { color: #ADFF2F; }
        .cibil { color: #FF69B4; }
        .assets { color: #8A2BE2; }
        
        /* Predict Button */
        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #28a745, #218838);
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        }

        div[data-testid="stButton"] > button:hover {
            transform: scale(1.1);
            background: linear-gradient(135deg, #218838, #28a745);
        }

        /* Loan Messages */
        .loan-approved {
            color: #2ecc71;
            font-weight: bold;
            font-size: 28px;
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            animation: fadeIn 1s ease-in-out;
        }

        .loan-rejected {
            color: #e74c3c;
            font-weight: bold;
            font-size: 28px;
            text-align: center;
            padding: 20px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            animation: shake 0.5s ease-in-out;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes shake {
            0% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            50% { transform: translateX(5px); }
            75% { transform: translateX(-5px); }
            100% { transform: translateX(0); }
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.header('💰✨ Loan Prediction App ✨🏦')

# Simple Instructions for All Users
st.markdown("""
### **🔍 How This App Works?**  
✔️ Enter **your details** below  
✔️ Click the **Predict Loan Status** button  
✔️ Get **Instant Loan Approval Result**  

---

### **📌 Fill in Your Details Below:**
""")

# User Input Fields with Large Icons
st.markdown('<div class="section-box education">🎓 **Are You Educated?** (Graduated / Not Graduated)</div>', unsafe_allow_html=True)
grad = st.selectbox('🎓 Education Level', ['Graduated', 'Not Graduated'])

st.markdown('<div class="section-box employment">💼 **Are You Self Employed?** (Yes / No)</div>', unsafe_allow_html=True)
self_emp = st.selectbox('💼 Self Employed?', ['Yes', 'No'])

st.markdown('<div class="section-box income">💰 **What is Your Annual Income?** (₹ Amount)</div>', unsafe_allow_html=True)
Annual_Income = st.number_input('💰 Annual Income (₹)', 0, 10000000)

st.markdown('<div class="section-box loan">🏦 **How Much Loan Do You Need?** (₹ Amount)</div>', unsafe_allow_html=True)
Loan_Amount = st.number_input('🏦 Loan Amount (₹)', 0, 10000000)

st.markdown('<div class="section-box cibil">📊 **What is Your CIBIL Score?** (300-900)</div>', unsafe_allow_html=True)
Cibil = st.number_input('📊 CIBIL Score', 300, 900)

st.markdown('<div class="section-box assets">🏡 **What Assets Do You Own?** (₹ Value)</div>', unsafe_allow_html=True)
Assets = st.number_input('🏡 Total Assets (₹)', 0, 10000000)

st.markdown('<div class="section-box loan">📆 **Loan Duration (Years)**</div>', unsafe_allow_html=True)
Loan_Dur = st.number_input('⏳ Loan Duration (Years)', 0, 20)

st.markdown('<div class="section-box employment">👨‍👩‍👧‍👦 **Number of Dependents**</div>', unsafe_allow_html=True)
no_of_dep = st.number_input('👨‍👩‍👧‍👦 No of Dependents', 0, 5)

# Encode Inputs
grad_s = 0 if grad == 'Graduated' else 1
emp_s = 0 if self_emp == 'No' else 1

# Prediction Button
if st.button("🔍 **Check Loan Status**"):
    pred_data = pd.DataFrame([[no_of_dep, grad_s, emp_s, Annual_Income, Loan_Amount, Loan_Dur, Cibil, Assets]],
                             columns=['no_of_dependents', 'education', 'self_employed', 'income_annum', 'loan_amount', 'loan_term', 'cibil_score', 'Assets'])
    pred_data = scaler.transform(pred_data)
    predict = model.predict(pred_data)

    if predict[0] == 1:
        st.markdown('<p class="loan-approved">✅ **Congratulations! Your Loan Is Approved.** 🎉</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="loan-rejected">❌ **Sorry! Your Loan Is Rejected.** 😞</p>', unsafe_allow_html=True)
