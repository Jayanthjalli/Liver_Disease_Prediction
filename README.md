# 🩺 Liver Disease Prediction System

A Machine Learning-based web application that predicts the possibility of liver disease using patient medical and blood-test data.

The application is built using **Python, Streamlit, XGBoost, Scikit-learn, Pandas, NumPy, SMOTE, and PDFPlumber**. It provides an interactive interface for user authentication, liver disease prediction, blood report upload, prediction history, and model insights.

---

## 📌 Project Overview

Liver diseases can be difficult to identify at an early stage because symptoms may not always be noticeable.

This project uses Machine Learning to analyze important medical parameters and predict whether a patient is likely to have liver disease.

The system uses the **Indian Liver Patient Dataset (ILPD)** and an **XGBoost Classifier** to perform the prediction.

Users can either manually enter medical values or upload a blood report in PDF format. The system extracts relevant values from the report and uses them for prediction.

> **Disclaimer:** This project is intended for educational and research purposes. It is not a medical diagnosis tool and should not replace advice from a qualified healthcare professional.

---

# 🚀 Features

### 🔐 User Authentication

* User registration
* User login
* User logout
* Session-based authentication
* Admin and normal-user access

### 🩺 Liver Disease Prediction

* XGBoost-based prediction
* Manual medical data entry
* Disease/Healthy prediction
* Prediction confidence percentage

### 📄 Blood Report Upload

* Upload blood reports in PDF format
* Extract medical values automatically using PDFPlumber
* Automatically populate prediction-related values
* Display extracted patient information

### 📊 Prediction History

* Store prediction results
* Store patient name
* Store prediction confidence
* Store prediction date and time
* Display prediction history in a table

### 🛠️ Admin Dashboard

* View registered users
* View prediction history
* Display disease statistics
* Monitor prediction results

### 📈 Model Insights

* Display Machine Learning feature importance
* Visualize important prediction features using charts

### 🎨 User Interface

* Streamlit-based web interface
* Dashboard navigation
* Responsive two-column prediction form
* Custom CSS styling
* Cards and visual sections

---

# 🧠 Machine Learning

The project uses an **XGBoost Classifier** for liver disease prediction.

### Dataset

The model is trained using:

**Indian Liver Patient Dataset (ILPD)**

Dataset file:


Indian Liver Patient Dataset (ILPD).csv


### Input Features

The model uses the following 10 features:

1. Age
2. Gender
3. Total Bilirubin
4. Direct Bilirubin
5. Alkaline Phosphotase
6. Alamine Aminotransferase
7. Aspartate Aminotransferase
8. Total Proteins
9. Albumin
10. Albumin and Globulin Ratio

### Target

The `Dataset column is used as the target variable.


1 → Liver Disease
2 → Healthy


The values are converted during preprocessing to:

1 → Disease
0 → Healthy


# 🔄 Machine Learning Workflow


Indian Liver Patient Dataset
            ↓
       Load Dataset
            ↓
      Data Preprocessing
            ↓
    Encode Gender Values
            ↓
   Handle Missing Values
            ↓
      Remove NaN Values
            ↓
       Apply SMOTE
            ↓
     Train/Test Split
            ↓
     XGBoost Classifier
            ↓
       Model Training
            ↓
      Model Evaluation
            ↓
      Save Model (.pkl)
            ↓
       Streamlit App
            ↓
       Liver Prediction

# 📄 PDF Blood Report Workflow

The application allows users to upload a blood report in PDF format.


Upload Blood Report
        ↓
    PDFPlumber
        ↓
Extract Text
        ↓
Identify Medical Values
        ↓
Auto-Fill Prediction Form
        ↓
XGBoost Prediction
        ↓
Display Result

The system attempts to extract:

* Patient Name
* Total Bilirubin
* Direct Bilirubin
* Alkaline Phosphotase
* ALT
* AST
* Total Proteins
* Albumin
* Albumin/Globulin Ratio


# 📂 Project Structure


LiverProject/
│
├── app.py
├── model.py
├── liver_model.pkl
│
├── Indian Liver Patient Dataset (ILPD).csv
│
├── users.json
├── history.json
│
├── Akashbloodreport.pdf
├── Documentation.pdf
├── presentation.pdf
│
├── .vscode/
│   └── settings.json
│
└── README.md

---

# 🛠️ Technologies Used

| Technology       | Purpose                             |
| ---------------- | ----------------------------------- |
| Python           | Application and Machine Learning    |
| Streamlit        | Web application interface           |
| XGBoost          | Machine Learning model              |
| Scikit-learn     | Model training and evaluation       |
| Pandas           | Data processing                     |
| NumPy            | Numerical operations                |
| Matplotlib       | Data visualization                  |
| Imbalanced-learn | SMOTE data balancing                |
| PDFPlumber       | PDF blood report extraction         |
| Joblib           | Model saving/loading                |
| JSON             | User and prediction history storage |

---

# ⚙️ Installation

## 1. Clone the Repository


git clone <your-github-repository-url>


Move into the project directory:


cd LiverProject


---

## 2. Create a Virtual Environment

Creating a virtual environment is recommended.

### Windows


python -m venv venv


Activate it:


venv\Scripts\activate


### Linux / macOS


python3 -m venv venv

Activate it:

source venv/bin/activate


---

# 📦 Install Dependencies

Install the required Python packages:

pip install streamlit pandas numpy matplotlib scikit-learn xgboost imbalanced-learn pdfplumber joblib


Or create a `requirements.txt` file containing:

streamlit
pandas
numpy
matplotlib
scikit-learn
xgboost
imbalanced-learn
pdfplumber
joblib

Then install:

pip install -r requirements.txt


---

# ▶️ Run the Application

Run the Streamlit application using:

streamlit run app.py


The application will normally be available at:


http://localhost:8501


---

# 🧪 Train the Machine Learning Model

The project already contains:


liver_model.pkl


If you want to retrain the model, run:


python model.py

The script will:

1. Load the ILPD dataset
2. Preprocess the data
3. Encode gender
4. Handle missing values
5. Balance the data using SMOTE
6. Split the dataset
7. Train the XGBoost model
8. Calculate prediction accuracy
9. Save the trained model as:

liver_model.pkl


---

# 🔑 Application Login

The application supports registration and login through the Streamlit interface.

Users can create an account using:

Register


and then log in using:

Login


The application stores user information in:

users.json


Prediction records are stored in:

history.json


> For a production application, passwords should be securely hashed and user data should be stored in a proper database instead of plain JSON files.

---

# 👨‍💼 Admin Dashboard

The application provides an Admin Panel with functionality to:

* View registered users
* View prediction history
* Analyze prediction results
* Display disease statistics

The application identifies the administrator based on the configured username.

> Do not publish real administrator credentials or sensitive account information in a public GitHub repository.

---

# 📊 Model Insights

The **Insights** section displays feature importance generated by the XGBoost model.

The system analyzes the importance of features such as:

Age
Gender
Total Bilirubin
Direct Bilirubin
Alkaline Phosphotase
Alamine Aminotransferase
Aspartate Aminotransferase
Total Proteins
Albumin
Albumin and Globulin Ratio

This helps visualize which input features contribute more to the model's predictions.

---

# 💾 Data Storage

The current project uses JSON files for lightweight local storage.

### Users


users.json


Stores registered users.

### Prediction History


history.json


Stores:

* Patient name
* Prediction result
* Confidence
* Date and time

For a production deployment, these should be replaced with a secure database.

---

# 🔒 Security Considerations

This project is primarily designed for learning and demonstration.

Before deploying it publicly, consider implementing:

* Password hashing
* Secure session management
* Database-backed authentication
* Input validation
* CSRF protection
* Secret management
* HTTPS
* Role-based authorization
* Secure file upload validation
* Removal of sensitive files from GitHub

---

# ⚠️ Important GitHub Note

Before pushing this project to GitHub, **do not upload sensitive or unnecessary files**, especially:

token.txt


If `token.txt` contains an API token, password, secret key, or other credential, remove it from the project and rotate/revoke the credential if it has ever been exposed.

You should also consider excluding:


.vscode/
.ipynb_checkpoints/
*.pyc
__pycache__/
venv/
.env
token.txt


using a `.gitignore` file.

---

# 📝 Recommended `.gitignore`

Create a file named:


.gitignore


and add:


# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual Environment
venv/
env/
.venv/

# Jupyter
.ipynb_checkpoints/

# VS Code
.vscode/

# Environment variables and secrets
.env
token.txt

# OS files
.DS_Store
Thumbs.db


---

# 🔮 Future Enhancements

The project can be further improved with:

* 🔐 Secure password hashing
* 🗄️ MySQL/PostgreSQL database
* 👨‍⚕️ Doctor dashboard
* 📧 Email prediction reports
* 📄 Automatic PDF report generation
* 🔎 OCR support for scanned blood reports
* 🤖 Comparison of multiple Machine Learning algorithms
* 📊 Advanced analytics dashboard
* 📱 Improved mobile UI
* ☁️ Cloud deployment
* 🔑 Password reset functionality
* 👤 User profile management
* 📈 Advanced model evaluation
* 🧪 Cross-validation
* ⚡ Model optimization

---

# 📈 Possible Machine Learning Improvements

Future versions could compare:


Logistic Regression
        ↓
Decision Tree
        ↓
Random Forest
        ↓
SVM
        ↓
Gradient Boosting
        ↓
XGBoost


and compare them using metrics such as:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

This would help identify the most suitable model for the dataset.

---

# 🎯 Project Objectives

The main objectives of this project are:

* To develop a Machine Learning-based liver disease prediction system.
* To provide a simple web interface for users.
* To reduce manual analysis of medical parameters.
* To support blood report PDF data extraction.
* To provide prediction confidence.
* To maintain prediction history.
* To visualize Machine Learning feature importance.
* To demonstrate the practical application of XGBoost in healthcare-related Machine Learning.

---

# 📜 Disclaimer

This application is developed for **educational and research purposes only**.

The predictions generated by this system should **not be considered a medical diagnosis**. Users should always consult a qualified healthcare professional for medical advice, diagnosis, and treatment.

---

# 👨‍💻 Author

** JAYANTH **

Developed as a Machine Learning project using Python, Streamlit, XGBoost, and the Indian Liver Patient Dataset.

---

# 📄 License

This project is intended for educational and research purposes.

You are free to modify and extend the project for learning and portfolio development.
