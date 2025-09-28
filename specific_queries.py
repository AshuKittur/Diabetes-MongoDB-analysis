from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['diabetes_project']
collection = db['patient_data']

print("=== SPECIFIC DIABETES DATA QUERIES ===")

def question_1_long_stay_patients():
    """Which patients stayed in hospital the longest?"""
    print("\n1. 🏥 PATIENTS WITH LONGEST HOSPITAL STAYS:")
    
    # Find top 10 longest stays
    longest_stays = collection.find().sort("time_in_hospital", -1).limit(10)
    
    for patient in longest_stays:
        print(f"   Patient {patient['patient_nbr']}: {patient['time_in_hospital']} days, "
              f"Age: {patient.get('age', 'N/A')}, Readmitted: {patient.get('readmitted', 'N/A')}")

def question_2_readmission_by_age():
    """What's the readmission rate by age group?"""
    print("\n2. 👴 READMISSION RATES BY AGE GROUP:")
    
    pipeline = [
        {"$group": {
            "_id": {"age": "$age", "readmitted": "$readmitted"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.age": 1}}
    ]
    
    results = list(collection.aggregate(pipeline))
    
    # Group by age
    age_groups = {}
    for result in results:
        age = result["_id"]["age"]
        readmission_status = result["_id"]["readmitted"]
        count = result["count"]
        
        if age not in age_groups:
            age_groups[age] = {}
        age_groups[age][readmission_status] = count
    
    # Print results
    for age, stats in age_groups.items():
        total = sum(stats.values())
        readmission_rate = (stats.get('YES', 0) + stats.get('>30', 0)) / total * 100
        print(f"   {age}: {readmission_rate:.1f}% readmission rate ({total} patients)")

def question_3_medication_analysis():
    """How many medications do patients typically take?"""
    print("\n3. 💊 MEDICATION ANALYSIS:")
    
    # Average medications
    avg_meds = list(collection.aggregate([
        {"$group": {"_id": None, "avg_medications": {"$avg": "$num_medications"}}}
    ]))[0]['avg_medications']
    
    print(f"   Average medications per patient: {avg_meds:.1f}")
    
    # Medication distribution
    med_distribution = list(collection.aggregate([
        {"$bucket": {
            "groupBy": "$num_medications",
            "boundaries": [0, 10, 20, 30, 40, 50],
            "default": "50+",
            "output": {"count": {"$sum": 1}}
        }}
    ]))
    
    print("   Medication distribution:")
    for bucket in med_distribution:
        print(f"     {bucket['_id']} meds: {bucket['count']} patients")

def question_4_insulin_impact():
    """Does insulin usage affect readmission?"""
    print("\n4. 💉 INSULIN IMPACT ON READMISSION:")
    
    pipeline = [
        {"$group": {
            "_id": {"insulin": "$insulin", "readmitted": "$readmitted"},
            "count": {"$sum": 1}
        }}
    ]
    
    results = list(collection.aggregate(pipeline))
    
    insulin_stats = {}
    for result in results:
        insulin = result["_id"]["insulin"]
        readmitted = result["_id"]["readmitted"]
        count = result["count"]
        
        if insulin not in insulin_stats:
            insulin_stats[insulin] = {"total": 0, "readmitted": 0}
        
        insulin_stats[insulin]["total"] += count
        if readmitted in ["YES", ">30"]:
            insulin_stats[insulin]["readmitted"] += count
    
    for insulin, stats in insulin_stats.items():
        if stats["total"] > 0:
            rate = stats["readmitted"] / stats["total"] * 100
            print(f"   {insulin}: {rate:.1f}% readmission rate")

def question_5_race_analysis():
    """Are there differences in treatment by race?"""
    print("\n5. 🌍 RACE ANALYSIS:")
    
    pipeline = [
        {"$group": {
            "_id": "$race",
            "avg_stay": {"$avg": "$time_in_hospital"},
            "avg_meds": {"$avg": "$num_medications"},
            "avg_labs": {"$avg": "$num_lab_procedures"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    
    results = list(collection.aggregate(pipeline))
    
    for result in results:
        if result["_id"]:  # Skip null/empty races
            print(f"   {result['_id']}:")
            print(f"     Patients: {result['count']}")
            print(f"     Avg stay: {result['avg_stay']:.1f} days")
            print(f"     Avg meds: {result['avg_meds']:.1f}")
            print(f"     Avg labs: {result['avg_labs']:.1f}")

# Run all questions
if __name__ == "__main__":
    question_1_long_stay_patients()
    question_2_readmission_by_age()
    question_3_medication_analysis()
    question_4_insulin_impact()
    question_5_race_analysis()