import pandas as pd
from model import train_model 

data = pd.read_csv('emails.csv') 
train_model(data)

print("Model training complete and saved as 'phishing_model.pkl'.")
