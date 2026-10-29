import streamlit as st
import pandas as pd
import joblib

# ─────────────────────────────────────────────────────────────
# MUST be the first Streamlit call in the script
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load model and scaler
model = joblib.load("svm_fraud_model.pkl")
scaler = joblib.load("scaler.pkl")

# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────
st.title("🛡️ Fraud Detection System")
st.caption("AI-powered real-time fraud screening for financial transactions.")
st.divider()

# ─────────────────────────────────────────────────────────────
# Inputs — split into two columns for a cleaner layout
# ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Transaction Details")
    transaction_amount = st.number_input("Transaction Amount", min_value=0.0, value=0.0)
    account_balance = st.number_input("Account Balance", min_value=0.0, value=0.0)
    transaction_type = st.selectbox(
        "Transaction Type",
        ["Bank Transfer", "Online", "POS"],
    )
    merchant_category = st.selectbox(
        "Merchant Category",
        ["Electronics", "Groceries", "Restaurants", "Travel"],
    )
    card_type = st.selectbox(
        "Card Type",
        ["Discover", "Mastercard", "Visa"],
    )
    card_age = st.number_input("Card Age (days)", min_value=0, value=0)

with col2:
    st.subheader("🔐 User & Risk Info")
    device_type = st.selectbox(
        "Device Type",
        ["Mobile", "Tablet"],
    )
    location = st.selectbox(
        "Location",
        ["Mumbai", "New York", "Sydney", "Tokyo"],
    )
    authentication_method = st.selectbox(
        "Authentication Method",
        ["OTP", "PIN", "Password"],
    )
    ip_flag = st.selectbox("IP Address Flag", [0, 1])
    prev_fraud = st.selectbox("Previous Fraudulent Activity", [0, 1])
    risk_score = st.number_input("Risk Score", min_value=0.0, max_value=1.0, value=0.0)

st.subheader("📊 Behavioral Features")
col3, col4 = st.columns(2)

with col3:
    daily_transaction_count = st.number_input("Daily Transaction Count", min_value=0, value=0)
    avg_transaction_amount_7d = st.number_input(
        "Average Transaction Amount (7 Days)", min_value=0.0, value=0.0
    )
    failed_transaction_count_7d = st.number_input(
        "Failed Transaction Count (7 Days)", min_value=0, value=0
    )

with col4:
    transaction_distance = st.number_input("Transaction Distance", min_value=0.0, value=0.0)
    hour = st.slider("Hour of Day", 0, 23, 12)
    day_of_week = st.selectbox(
        "Day of Week",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"],
    )

st.divider()

# ─────────────────────────────────────────────────────────────
# Predict
# ─────────────────────────────────────────────────────────────
if st.button("🔍 Predict Fraud", type="primary", use_container_width=True):

    # Base numeric + binary features
    data = {
        "Transaction_Amount": transaction_amount,
        "Account_Balance": account_balance,
        "IP_Address_Flag": ip_flag,
        "Previous_Fraudulent_Activity": prev_fraud,
        "Daily_Transaction_Count": daily_transaction_count,
        "Avg_Transaction_Amount_7d": avg_transaction_amount_7d,
        "Failed_Transaction_Count_7d": failed_transaction_count_7d,
        "Card_Age": card_age,
        "Transaction_Distance": transaction_distance,
        "Risk_Score": risk_score,
        "Hour": hour,

        # One-hot placeholders (all zero by default)
        "Transaction_Type_Bank Transfer": 0,
        "Transaction_Type_Online": 0,
        "Transaction_Type_POS": 0,

        "Device_Type_Mobile": 0,
        "Device_Type_Tablet": 0,

        "Location_Mumbai": 0,
        "Location_New York": 0,
        "Location_Sydney": 0,
        "Location_Tokyo": 0,

        "Merchant_Category_Electronics": 0,
        "Merchant_Category_Groceries": 0,
        "Merchant_Category_Restaurants": 0,
        "Merchant_Category_Travel": 0,

        "Card_Type_Discover": 0,
        "Card_Type_Mastercard": 0,
        "Card_Type_Visa": 0,

        "Authentication_Method_OTP": 0,
        "Authentication_Method_PIN": 0,
        "Authentication_Method_Password": 0,

        "Day_of_Week_Monday": 0,
        "Day_of_Week_Saturday": 0,
        "Day_of_Week_Sunday": 0,
        "Day_of_Week_Thursday": 0,
        "Day_of_Week_Tuesday": 0,
        "Day_of_Week_Wednesday": 0,
    }

    # Set the selected category's dummy to 1
    data[f"Transaction_Type_{transaction_type}"] = 1
    data[f"Device_Type_{device_type}"] = 1
    data[f"Location_{location}"] = 1
    data[f"Merchant_Category_{merchant_category}"] = 1
    data[f"Card_Type_{card_type}"] = 1
    data[f"Authentication_Method_{authentication_method}"] = 1
    data[f"Day_of_Week_{day_of_week}"] = 1

    input_df = pd.DataFrame([data])

    # ── Column-order safety: match the order the model was trained on ──
    try:
        expected_cols = list(scaler.feature_names_in_)
        input_df = input_df[expected_cols]
    except AttributeError:
        # Older sklearn scalers don't expose feature_names_in_ — skip the reorder
        pass

    # Scale
    input_scaled = scaler.transform(input_df)

    # Predict
    prediction = model.predict(input_scaled)

    # Probability (SVC needs probability=True at fit time to expose this)
    probability = None
    if hasattr(model, "predict_proba"):
        try:
            probability = model.predict_proba(input_scaled)[0][1]
        except Exception:
            probability = None

    # ─────────────────────────────────────────────────────────
    # Result
    # ─────────────────────────────────────────────────────────
    st.subheader("🧾 Prediction Result")

    if prediction[0] == 1:
        st.error("🚨 **Fraudulent Transaction Detected**")
        if probability is not None:
            st.metric("Fraud Probability", f"{probability:.2%}")
    else:
        st.success("✅ **Legitimate Transaction**")
        if probability is not None:
            st.metric("Fraud Probability", f"{probability:.2%}")

    # Show the raw inputs in an expander for transparency
    with st.expander("🔎 View input summary"):
        st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)


        #TXN_36537   USER_7333   124.74  Bank Transfer  sunday  14:40:00 61520.85 Tablet Mumbai Travel