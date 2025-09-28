from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['diabetes_project']
collection = db['patient_data']

print("===DIABETES DATA ANALYSIS===")

#1. Basic Statistics
total = collection.count_documents({})
print(f"Total Patients: {total}")

# 2. Readmission analysis
readmission_stats = list(collection.aggregate([
    {"$group": {"_id": "$readmitted", "count": {"$sum": 1}}}
]))
print("\n📈 Readmission rates:")
for stat in readmission_stats:
    percentage = (stat['count'] / total) * 100
    print(f"   {stat['_id']}: {stat['count']} patients ({percentage:.1f}%)")

# 3. Average hospital stay
avg_stay = list(collection.aggregate([
    {"$group": {"_id": None, "avg_stay": {"$avg": "$time_in_hospital"}}}
]))[0]['avg_stay']
print(f"🏥 Average hospital stay: {avg_stay:.1f} days")