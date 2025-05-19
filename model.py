import pandas as pd
import numpy as np
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from utils import clean_email_body, extract_url_features

# load and train the model
def train_model(data):
    # Clean and process email bodies
    data['cleaned_body'] = data['email_body'].apply(clean_email_body)
    data['url_features'] = data['email_body'].apply(extract_url_features)

    X = pd.concat([data['cleaned_body'], data['url_features']], axis=1)
    X.columns = ['email_body', 'url_features']
    y = data['label']

    body_vectorizer = CountVectorizer()
    model = make_pipeline(body_vectorizer, MultinomialNB())

    # Train the model
    model.fit(X['email_body'], y)
    
    # Save the trained model
    joblib.dump(model, 'phishing_model.pkl')

def predict_phishing(model, email_body):
    cleaned_body = clean_email_body(email_body)
    url_features = extract_url_features(email_body)
    X = pd.DataFrame([[cleaned_body, url_features]], columns=['email_body', 'url_features'])
    
    # Predict using the trained model
    # Note - Im not using url in my prediction because of an error. I intend to fix it soon
    prediction = model.predict(X['email_body'])
    return 'Phishing' if prediction[0] == 1 else 'Safe'
