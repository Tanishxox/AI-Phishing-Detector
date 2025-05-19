import re
import numpy as np
from urllib.parse import urlparse
import requests
from nltk.corpus import stopwords

# Download NLTK data
import nltk
nltk.download('stopwords')

# Load stopwords
STOPWORDS = set(stopwords.words("english"))

# Function to clean and process the email body
def clean_email_body(email_body):
    # Removing non-alphabetic characters
    email_body = re.sub(r'[^a-zA-Z\s]', '', email_body)
    # Lowercasing and removing stopwords
    email_body = ' '.join([word.lower() for word in email_body.split() if word.lower() not in STOPWORDS])
    return email_body

def extract_url_features(email_body):
    urls = re.findall(r'(https?://[^\s]+)', email_body)
    features = []
    
    for url in urls:
        parsed_url = urlparse(url)
        
        # Ensure numeric values are appended to the features list
        domain_length = len(parsed_url.netloc)  # Length of the domain
        path_length = len(parsed_url.path)  # Length of the path
        protocol = parsed_url.scheme  # Protocol (http/https)
        
        features.append(domain_length)
        features.append(path_length)
        
        # Check if the protocol is valid and append to features
        if protocol in ['http', 'https']:
            features.append(1)
        else:
            features.append(0)
        
        # Try to fetch the URL to check its status code
        try:
            response = requests.get(url, timeout=3)
            status_code = response.status_code
            features.append(status_code)
        except:
            features.append(0)  # If URL is not reachable, append 0
    
    # Return the mean of numeric values in the features list or 0 if empty
    return np.mean([f for f in features if isinstance(f, (int, float))]) if features else 0
