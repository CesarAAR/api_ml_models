import pandas as pd 
import pickle

with open("ml_models\\scaler_fraud.pkl", "rb") as f:
    scaler = pickle.load(f)

def elt_transform(json_data):

    df = pd.DataFrame([json_data] if isinstance(json_data, dict) else json_data)

    df[['Time', 'Amount']] = scaler.transform(df[['Time', 'Amount']])

    return df