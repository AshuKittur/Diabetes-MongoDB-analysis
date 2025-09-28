# explore_data.py
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['diabetes_project']
collection = db['patient_data']

print("Connected to MongoDB!")
print(f"Total patients: {collection.count_documents({})}")
