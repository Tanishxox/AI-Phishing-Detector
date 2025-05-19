# AI-Powered Phishing Email Detector

## Overview
The **AI-Powered Phishing Email Detector** is a machine learning-based application designed to analyze email content and determine whether an email is **Phishing** or **Not Phishing**. The system leverages Natural Language Processing (NLP) techniques and a trained model to classify emails in real-time.

## Features
- **Real-time Phishing Detection**: Analyze email body content and classify it as phishing or safe.
- **Interactive Web Interface**: Built using **Streamlit** for an intuitive and user-friendly experience.
- **Machine Learning Model**: Uses NLP-based feature extraction and a trained classifier (e.g., Random Forest, SVM, or other ML models).
- **Visual Feedback**: Displays an appropriate image based on the prediction (Phishing or Not Phishing).
- **Secure API Integration**: Integration with email services for  email scanning.

## Installation

### Prerequisites
Make sure you have **Python 3.8+** installed on your system.

### Step 1: Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### Step 2: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Train the Model (If Not Provided)
If the trained model (`phishing_model.pkl`) is not included, train it using:
```sh
python train_model.py
```

### Step 5: Run the Application
```sh
streamlit run main.py
```

## Usage
1. **Launch the Streamlit app.**
2. **Enter the email body** in the provided text area or connect to your gmail account and select an email from the dropdown.
3. Click the **"Analyze Email"** button.
4. The application will process the email and return:
   - A text-based prediction (**Phishing** or **Not Phishing**).


## Technologies Used
- **Python 3.8+**
- **Streamlit** (Frontend UI)
- **Scikit-learn** (Machine Learning)
- **NLTK / spaCy** (Natural Language Processing)
- **Joblib** (Model Serialization)
- **Pandas & NumPy** (Data Processing)

   
