import streamlit as st
import joblib
import numpy as np
import pandas as pd
import datetime
import mysql.connector
from mysql.connector import Error
import pdfplumber
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Liver Disease Prediction",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.card {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    padding: 20px;
}

.title {
    color: #2c3e50;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "liver_project"
}


# ============================================================
# MYSQL CONNECTION
# ============================================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )

        return connection

    except Error as e:

        st.error(
            f"MySQL connection failed: {e}"
        )

        return None


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    try:

        # Connect without selecting database
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        cursor = connection.cursor()

        # Create database
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS liver_project"
        )

        cursor.execute(
            "USE liver_project"
        )

        # ----------------------------------------------------
        # USERS TABLE
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INT AUTO_INCREMENT PRIMARY KEY,

                username VARCHAR(100) NOT NULL UNIQUE,

                password VARCHAR(255) NOT NULL,

                role VARCHAR(20) NOT NULL DEFAULT 'user',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        # ----------------------------------------------------
        # PREDICTION HISTORY TABLE
        # ----------------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (

                id INT AUTO_INCREMENT PRIMARY KEY,

                username VARCHAR(100) NOT NULL,

                patient_name VARCHAR(255)
                    DEFAULT 'Unknown',

                result VARCHAR(50) NOT NULL,

                confidence DECIMAL(5,2) NOT NULL,

                prediction_time DATETIME
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (username)
                    REFERENCES users(username)

                    ON DELETE CASCADE

                    ON UPDATE CASCADE

            )
        """)

        # ----------------------------------------------------
        # DEFAULT USERS
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO users
            (username, password, role)

            VALUES
            ('admin', '12345', 'admin'),
            ('ganesh', '12345', 'user'),
            ('ravi', '123', 'user')

            ON DUPLICATE KEY UPDATE

                password = VALUES(password),

                role = VALUES(role)
        """)

        connection.commit()

        cursor.close()
        connection.close()

        return True

    except Error as e:

        st.error(
            "Unable to initialize MySQL database.\n\n"
            f"Error: {e}"
        )

        return False


# ============================================================
# INITIALIZE DATABASE
# ============================================================

if not initialize_database():

    st.stop()


# ============================================================
# LOAD ML MODEL
# ============================================================

try:

    model = joblib.load(
        "liver_model.pkl"
    )

except Exception as e:

    st.error(
        "liver_model.pkl could not be loaded."
    )

    st.info(
        "Run this command first:\n\n"
        "python model.py"
    )

    st.exception(e)

    st.stop()


# ============================================================
# USER FUNCTIONS
# ============================================================

def register_user(username, password):

    username = username.strip()

    if not username or not password:

        return False, "Username and password are required."

    connection = get_db_connection()

    if connection is None:

        return False, "Database connection failed."

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (username, password, role)

            VALUES
            (%s, %s, 'user')
        """, (
            username,
            password
        ))

        connection.commit()

        return True, "Account created successfully!"

    except Error as e:

        connection.rollback()

        # Duplicate username
        if getattr(e, "errno", None) == 1062:

            return False, "Username already exists."

        return False, f"Registration failed: {e}"

    finally:

        cursor.close()
        connection.close()


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login_user(username, password):

    connection = get_db_connection()

    if connection is None:

        return None

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT
                username,
                role

            FROM users

            WHERE username = %s
            AND password = %s
        """, (
            username,
            password
        ))

        user = cursor.fetchone()

        return user

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SAVE PREDICTION HISTORY
# ============================================================

def save_history(record):

    connection = get_db_connection()

    if connection is None:

        return False

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO prediction_history
            (
                username,
                patient_name,
                result,
                confidence,
                prediction_time
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (

            st.session_state.username,

            record.get(
                "patient_name",
                "Unknown"
            ),

            record["result"],

            record["confidence"],

            record.get(
                "time",
                datetime.datetime.now()
            )

        ))

        connection.commit()

        return True

    except Error as e:

        connection.rollback()

        st.error(
            f"Could not save prediction: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()


# ============================================================
# LOAD HISTORY
# ============================================================

def load_history(username=None):

    connection = get_db_connection()

    if connection is None:

        return []

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        if username:

            cursor.execute("""
                SELECT

                    id,

                    username,

                    patient_name,

                    result,

                    confidence,

                    prediction_time

                FROM prediction_history

                WHERE username = %s

                ORDER BY prediction_time DESC
            """, (
                username,
            ))

        else:

            cursor.execute("""
                SELECT

                    id,

                    username,

                    patient_name,

                    result,

                    confidence,

                    prediction_time

                FROM prediction_history

                ORDER BY prediction_time DESC
            """)

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# ============================================================
# LOAD USERS
# ============================================================

def load_users():

    connection = get_db_connection()

    if connection is None:

        return []

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute("""
            SELECT

                id,

                username,

                role,

                created_at

            FROM users

            ORDER BY id
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = ""


if "role" not in st.session_state:

    st.session_state.role = "user"


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🧭 Navigation"
)


if st.session_state.logged_in:

    if st.session_state.role == "admin":

        page = st.sidebar.radio(
            "Go to",
            [
                "Home",
                "Prediction",
                "Insights",
                "Admin Panel",
                "Logout"
            ]
        )

    else:

        page = st.sidebar.radio(
            "Go to",
            [
                "Home",
                "Prediction",
                "Insights",
                "My History",
                "Logout"
            ]
        )

else:

    page = st.sidebar.radio(
        "Go to",
        [
            "Login",
            "Register"
        ]
    )


# ============================================================
# LOGIN
# ============================================================

if page == "Login":

    st.markdown(
        "<h1 class='title'>🔐 Login</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            username,
            password
        )

        if user:

            st.success(
                "Login Successful!"
            )

            st.session_state.logged_in = True

            st.session_state.username = \
                user["username"]

            st.session_state.role = \
                user["role"]

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# REGISTER
# ============================================================

elif page == "Register":

    st.markdown(
        "<h1 class='title'>📝 Register</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )

    new_user = st.text_input(
        "Create Username"
    )

    new_pass = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Register"):

        success, message = register_user(
            new_user,
            new_pass
        )

        if success:

            st.success(message)

        else:

            st.error(message)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# HOME
# ============================================================

elif page == "Home":

    st.markdown(
        "<h1 class='title'>🏠 Dashboard</h1>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "<div class='card'>",
            unsafe_allow_html=True
        )

        st.subheader(
            "📊 Project Info"
        )

        st.write(
            "This system predicts liver disease "
            "using Machine Learning (XGBoost)."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            "<div class='card'>",
            unsafe_allow_html=True
        )

        st.subheader(
            "⚡ Features"
        )

        st.write(
            "✔ Fast Prediction\n"
            "✔ Easy UI\n"
            "✔ Medical Decision Support"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# PREDICTION
# ============================================================

elif page == "Prediction":

    st.markdown(
        "<h1 class='title'>🩺 Prediction</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

    with col1:

        age = st.number_input(
            "Age",
            min_value=0.0,
            value=1.0
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female"
            ]
        )

        tb = st.number_input(
            "Total Bilirubin",
            min_value=0.0
        )

        db = st.number_input(
            "Direct Bilirubin",
            min_value=0.0
        )

        alk = st.number_input(
            "Alkaline Phosphotase",
            min_value=0.0
        )

    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

    with col2:

        alt = st.number_input(
            "Alamine Aminotransferase",
            min_value=0.0
        )

        ast = st.number_input(
            "Aspartate Aminotransferase",
            min_value=0.0
        )

        tp = st.number_input(
            "Total Proteins",
            min_value=0.0
        )

        alb = st.number_input(
            "Albumin",
            min_value=0.0
        )

        agr = st.number_input(
            "Albumin and Globulin Ratio",
            min_value=0.0
        )


    # ========================================================
    # PDF UPLOAD
    # ========================================================

    st.subheader(
        "📄 Upload Blood Report (PDF)"
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )


    # ========================================================
    # PDF EXTRACTION
    # ========================================================

    def extract_pdf(file):

        text = ""

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                text += (
                    page.extract_text()
                    or ""
                )

                text += "\n"


        def find(pattern):

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                return float(
                    match.group(1)
                )

            return None


        name_match = re.search(

            r"(?:Patient Name|Name)"
            r"\s*[:\-]?\s*"
            r"([A-Za-z ]+)",

            text,

            re.IGNORECASE
        )


        patient_name = (

            name_match.group(1).strip()

            if name_match

            else "Unknown"

        )


        return {

            "patient_name":
                patient_name,

            "Total_Bilirubin":
                find(
                    r"Total Bilirubin.*?"
                    r"(\d+\.?\d*)"
                ),

            "Direct_Bilirubin":
                find(
                    r"Direct Bilirubin.*?"
                    r"(\d+\.?\d*)"
                ),

            "Alkaline_Phosphotase":
                find(
                    r"Alkaline.*?"
                    r"(\d+\.?\d*)"
                ),

            "Alamine_Aminotransferase":
                find(
                    r"ALT.*?"
                    r"(\d+\.?\d*)"
                ),

            "Aspartate_Aminotransferase":
                find(
                    r"AST.*?"
                    r"(\d+\.?\d*)"
                ),

            "Total_Protiens":
                find(
                    r"Total Proteins.*?"
                    r"(\d+\.?\d*)"
                ),

            "Albumin":
                find(
                    r"Albumin.*?"
                    r"(\d+\.?\d*)"
                ),

            "Albumin_and_Globulin_Ratio":
                find(
                    r"A/G Ratio.*?"
                    r"(\d+\.?\d*)"
                )

        }


    # ========================================================
    # PROCESS PDF
    # ========================================================

    patient_name = "Manual Entry"


    if uploaded_file:

        data_pdf = extract_pdf(
            uploaded_file
        )

        st.json(
            data_pdf
        )

        patient_name = data_pdf.get(
            "patient_name",
            "Unknown"
        )


        # AUTO-FILL

        if data_pdf[
            "Total_Bilirubin"
        ] is not None:

            tb = data_pdf[
                "Total_Bilirubin"
            ]


        if data_pdf[
            "Direct_Bilirubin"
        ] is not None:

            db = data_pdf[
                "Direct_Bilirubin"
            ]


        if data_pdf[
            "Alkaline_Phosphotase"
        ] is not None:

            alk = data_pdf[
                "Alkaline_Phosphotase"
            ]


        if data_pdf[
            "Alamine_Aminotransferase"
        ] is not None:

            alt = data_pdf[
                "Alamine_Aminotransferase"
            ]


        if data_pdf[
            "Aspartate_Aminotransferase"
        ] is not None:

            ast = data_pdf[
                "Aspartate_Aminotransferase"
            ]


        if data_pdf[
            "Total_Protiens"
        ] is not None:

            tp = data_pdf[
                "Total_Protiens"
            ]


        if data_pdf[
            "Albumin"
        ] is not None:

            alb = data_pdf[
                "Albumin"
            ]


        if data_pdf[
            "Albumin_and_Globulin_Ratio"
        ] is not None:

            agr = data_pdf[
                "Albumin_and_Globulin_Ratio"
            ]


        st.success(
            "✅ PDF data loaded"
        )


    # ========================================================
    # PREDICT
    # ========================================================

    if st.button("Predict"):

        gender_val = (
            1
            if gender == "Male"
            else 0
        )


        values = [
            tb,
            db,
            alk,
            alt,
            ast,
            tp,
            alb,
            agr
        ]


        if any(
            value is None
            for value in values
        ):

            st.error(
                "❌ Some values are missing. "
                "Please check the input/report."
            )

            st.stop()


        # MODEL INPUT

        data = np.array([

            [
                age,
                gender_val,
                tb,
                db,
                alk,
                alt,
                ast,
                tp,
                alb,
                agr
            ]

        ])


        try:

            # Prediction

            result = model.predict(
                data
            )


            # Probability

            probability = \
                model.predict_proba(data)


            prediction_class = \
                int(result[0])


            confidence = (
                probability[0]
                [prediction_class]
                * 100
            )


            label = (

                "Disease"

                if prediction_class == 1

                else "Healthy"

            )


            # SAVE MYSQL

            saved = save_history({

                "patient_name":
                    patient_name,

                "result":
                    label,

                "confidence":
                    float(confidence),

                "time":
                    datetime.datetime.now()

            })


            # DISPLAY RESULT

            if prediction_class == 1:

                st.error(
                    "⚠ Liver Disease Detected"
                )

            else:

                st.success(
                    "✅ Healthy"
                )


            st.info(
                f"Prediction Confidence: "
                f"{confidence:.2f}%"
            )


            if saved:

                st.success(
                    "✅ Prediction saved to MySQL database."
                )


        except Exception as e:

            st.error(
                "Prediction failed."
            )

            st.exception(e)


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# MY HISTORY
# ============================================================

elif page == "My History":

    st.markdown(
        "<h1 class='title'>📜 My Prediction History</h1>",
        unsafe_allow_html=True
    )


    history = load_history(
        st.session_state.username
    )


    if history:

        df = pd.DataFrame(
            history
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No history found"
        )


# ============================================================
# ADMIN PANEL
# ============================================================

elif page == "Admin Panel":

    st.markdown(
        "<h1 class='title'>🛠 Admin Dashboard</h1>",
        unsafe_allow_html=True
    )


    # USERS

    users = load_users()

    st.subheader(
        "👥 Users"
    )


    if users:

        users_df = pd.DataFrame(
            users
        )

        st.dataframe(
            users_df,
            use_container_width=True
        )

    else:

        st.info(
            "No users found."
        )


    # HISTORY

    st.subheader(
        "📜 All Prediction History"
    )


    history = load_history()


    if history:

        df = pd.DataFrame(
            history
        )

        st.dataframe(
            df,
            use_container_width=True
        )


        st.subheader(
            "📊 Prediction Results"
        )

        st.bar_chart(
            df["result"].value_counts()
        )

    else:

        st.info(
            "No prediction history found."
        )


# ============================================================
# INSIGHTS
# ============================================================

elif page == "Insights":

    st.markdown(
        "<h1 class='title'>📊 Model Insights</h1>",
        unsafe_allow_html=True
    )


    try:

        features = [

            "Age",

            "Gender",

            "Total_Bilirubin",

            "Direct_Bilirubin",

            "Alkaline_Phosphotase",

            "Alamine_Aminotransferase",

            "Aspartate_Aminotransferase",

            "Total_Protiens",

            "Albumin",

            "Albumin_and_Globulin_Ratio"

        ]


        df_imp = pd.DataFrame({

            "Feature":
                features,

            "Importance":
                model.feature_importances_

        })


        df_imp = df_imp.sort_values(

            by="Importance",

            ascending=False

        )


        st.bar_chart(
            df_imp.set_index(
                "Feature"
            )
        )


    except Exception:

        st.warning(
            "Feature importance not available"
        )


# ============================================================
# LOGOUT
# ============================================================

elif page == "Logout":

    st.session_state.logged_in = False

    st.session_state.username = ""

    st.session_state.role = "user"

    st.success(
        "Logged out successfully!"
    )

    st.rerun()