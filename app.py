import streamlit as st
import pandas as pd
import io
import hashlib
import base64

st.set_page_config(page_title="Cloud Cost Leak Finder", layout="wide")

for key, default in {
    "users": {},
    "current_user": None,
    "role": None,
    "uploaded_data": None,
    "analysis_results": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, role):
    if username and password:
        if username not in st.session_state.users:
            st.session_state.users[username] = {
                "password": hash_password(password),
                "role": role,
            }
        else:
            st.warning("Username already exists.")
    else:
        st.error("Please provide both username and password.")

def authenticate(username, password):
    user_data = st.session_state.users.get(username)
    if user_data and user_data["password"] == hash_password(password):
        st.session_state.current_user = username
        st.session_state.role = user_data["role"]
        return True
    return False

def logout():
    st.session_state.current_user = None
    st.session_state.role = None
    st.session_state.uploaded_data = None
    st.session_state.analysis_results = None

def upload_csv():
    file = st.file_uploader("Upload Cloud Usage CSV", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file)
            required_cols = {"CPU_Usage", "Storage_Usage", "Cost"}
            if not required_cols.issubset(df.columns):
                st.error(f"CSV must contain columns: {', '.join(required_cols)}")
                return
            st.session_state.uploaded_data = df
            st.success("File uploaded successfully.")
        except Exception as e:
            st.error(f"Error reading file: {e}")

def analyze_data():
    df = st.session_state.uploaded_data.copy()
    df["CPU_Usage"] = df["CPU_Usage"].fillna(0)
    df["Storage_Usage"] = df["Storage_Usage"].fillna(0)
    df["Idle"] = df["CPU_Usage"] < 5
    df["Oversized"] = df["CPU_Usage"] < 30
    df["Underutilized_Storage"] = df["Storage_Usage"] < 20
    df["Risk_Score"] = (
        (df["CPU_Usage"].apply(lambda x: 100 - x) + df["Storage_Usage"].apply(lambda x: 100 - x)) / 2
    )
    df["Potential_Savings_Monthly"] = df["Cost"] * (df["Risk_Score"] / 100)
    df["Potential_Savings_Yearly"] = df["Potential_Savings_Monthly"] * 12
    st.session_state.analysis_results = df

def download_link(df):
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="cloud_cost_analysis.csv">Download CSV Report</a>'
    return href

st.title("Cloud Cost Leak Finder")

menu = ["Login", "Register", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register New User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["System Administrator", "Cloud Administrator"])
    if st.button("Register"):
        register_user(username, password, role)
        st.success("User registered successfully.")

elif choice == "Login":
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome {username}")
        else:
            st.error("Invalid credentials.")

elif choice == "Dashboard":
    if not st.session_state.current_user:
        st.warning("Please log in to access the dashboard.")
    else:
        st.sidebar.write(f"Logged in as: {st.session_state.current_user} ({st.session_state.role})")
        if st.sidebar.button("Logout"):
            logout()
            st.experimental_rerun()

        if st.session_state.role == "System Administrator":
            st.subheader("User Management")
            st.dataframe(pd.DataFrame.from_dict(st.session_state.users, orient="index"))

        elif st.session_state.role == "Cloud Administrator":
            st.subheader("Upload Cloud Usage Data")
            upload_csv()
            if st.session_state.uploaded_data is not None:
                st.dataframe(st.session_state.uploaded_data.head(), use_container_width=True)
                if st.button("Run Analysis"):
                    analyze_data()
            if st.session_state.analysis_results is not None:
                df = st.session_state.analysis_results
                st.subheader("Anomaly Detection & Savings Report")
                st.dataframe(df, use_container_width=True)
                total_monthly = df["Potential_Savings_Monthly"].sum()
                total_yearly = df["Potential_Savings_Yearly"].sum()
                st.metric("Total Potential Monthly Savings", f"${total_monthly:,.2f}")
                st.metric("Total Potential Yearly Savings", f"${total_yearly:,.2f}")
                st.markdown(download_link(df), unsafe_allow_html=True)
