import streamlit as st
import joblib
from model import predict_phishing
from utils import clean_email_body, extract_url_features
from gmail_auth import authenticate_gmail, fetch_latest_emails 

st.markdown("""
    <style>
        .title {
            font-size: 50px;
            color: #333333;  /* Dark gray for contrast */
            text-align: center;
            margin-top: 30px;
        }
        .stRadio > div {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 20px 0;
        }

        .stRadio > div > label > div:first-child {
            background-color: #e8f5e9 !important;
            border: 1px solid #2e7d32 !important;
            color: #1b5e20 !important
        }


        .stTextArea textarea {
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #888888;  
            background-color: rgba(255, 255, 255, 0.9);
            width: 100%;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .stButton > button {
            font-size: 18px;
            padding: 12px 30px;
            background-color: #66bb6a;  /* Green button */
            color: white;
            border: none;
            border-radius: 10px;
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #388e3c;
            color: white;
            transform: scale(1.05);
        }
    
        .stButton > button:focus,
        .stButton > button:focus-visible {
            color: white !important;  
            outline: none;
            box-shadow: none;
        }

        .stButton > button:active {
            color: white !important;  
        }

        .stButton {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }

        .header {
            font-size: 35px;
            color: #333333;
            text-align: center;
            padding: 10px;
        }

        .stContainer {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }

        .stColumn {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .stImage {
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .prediction-text {
            font-size: 22px; 
            color: #333333;
            text-align: center;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def clean_email_text(text):
    """Clean email text by removing HTML tags, images, and unnecessary patterns"""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\[image:[^\]]+\]', '', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def main():
    if 'emails_fetched' not in st.session_state:
        st.session_state.emails_fetched = False
    if 'email_options' not in st.session_state:
        st.session_state.email_options = {}
    if 'selected_email' not in st.session_state:
        st.session_state.selected_email = ""
    if 'input_mode' not in st.session_state:
        st.session_state.input_mode = "custom"  
    
    result = None
    
    st.markdown('<div class="header">AI-Powered Phishing Detector</div>', unsafe_allow_html=True)
    
    # Load trained model if available
    try:
        model = joblib.load('phishing_model.pkl')
        st.success("Model loaded successfully!")
    except:
        st.error("No trained model found. Please train the model first.")
    
    # Input mode selector
    input_mode = st.radio(
        "Choose input method:",
        ("📧 Enter custom email", "📥 Fetch from Gmail"),
        horizontal=True,
        index=0 if st.session_state.input_mode == "custom" else 1
    )
    
    st.session_state.input_mode = "custom" if input_mode == "📧 Enter custom email" else "gmail"
    
    if st.session_state.input_mode == "gmail":
        st.markdown("### Select an email from your Gmail account")
        
        # columns for better button layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Connect to Gmail"):
                try:
                    with st.spinner('Fetching your emails...'):
                        # Authenticate and fetch emails
                        service = authenticate_gmail()
                        emails = fetch_latest_emails(service, max_results=10)
                        
                        st.session_state.email_options = {
                            f"{email['subject'][:50]}...": clean_email_text(email['body']) 
                            for email in emails
                        }
                        st.session_state.emails_fetched = True
                        if st.session_state.email_options:
                            st.session_state.selected_email = list(st.session_state.email_options.keys())[0]
                            st.success(f"Fetched {len(st.session_state.email_options)} emails!")
                            time.sleep(1)
                        else:
                            st.warning("No emails found in your inbox")
                            
                except Exception as e:
                    st.error(f"Failed to connect to Gmail: {str(e)}")
        
        # Show email selection only if emails were fetched
        if st.session_state.emails_fetched and st.session_state.email_options:
            with col2:
                selected_subject = st.selectbox(
                    "Choose an email to analyze:",
                    options=list(st.session_state.email_options.keys()),
                    index=0,
                    key="email_selector"
                )
                st.session_state.selected_email = st.session_state.email_options[selected_subject]
    
    # Email Input (custom or from Gmail)
    email_input = st.text_area(
        "Email Content:", 
        value=st.session_state.selected_email if st.session_state.input_mode == "gmail" else "", 
        height=400, 
        help="Enter or paste the email content you want to analyze for phishing."
    )
    
    if st.button("Analyze Email", type="primary"):
        if email_input:
            with st.spinner('Analyzing email content...'):
                result = predict_phishing(model, email_input)
                if result == 'Phishing':
                    st.markdown(
                        f'<div class="prediction-text" style="color: #d32f2f;">'
                        f'⚠️ Warning: This email appears to be PHISHING!'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                    st.warning("Do not click any links or download attachments from suspicious emails!")
                else:
                    st.markdown(
                        f'<div class="prediction-text" style="color: #388e3c;">'
                        f'✅ This email appears to be SAFE'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                    st.info("Always remain cautious with unexpected emails, even if they appear safe.")
            
                with st.expander("Analysis Details"):
                    st.write("Email length:", len(email_input))
                    st.write("Cleaned content sample:", email_input[:200] + "...")
        else:
            st.warning("Please enter an email body for analysis.")

if __name__ == '__main__':
    main()