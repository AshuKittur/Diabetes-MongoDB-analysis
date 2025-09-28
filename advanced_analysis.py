"""
Advanced Analytics for Diabetes Readmission Prediction
Working version with proper error handling
"""
from pymongo import MongoClient

class AdvancedDiabetesAnalysis:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.collection = self.client['diabetes_project']['patient_data']
        print("✅ Advanced Analysis initialized")
    
    def predict_readmission_risk(self):
        """Identify factors correlated with readmission"""
        print("\n🔍 Analyzing readmission risk factors...")
        
        try:
            pipeline = [
                {"$match": {"readmitted": {"$in": ["YES", "NO"]}}},
                {"$group": {
                    "_id": "$readmitted",
                    "avg_medications": {"$avg": "$num_medications"},
                    "avg_stay": {"$avg": "$time_in_hospital"},
                    "avg_lab_procedures": {"$avg": "$num_lab_procedures"},
                    "patient_count": {"$sum": 1}
                }},
                {"$sort": {"patient_count": -1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            print("📊 Readmission Risk Analysis Results:")
            for result in results:
                readmission_status = result['_id']
                count = result['patient_count']
                avg_meds = result['avg_medications']
                avg_stay = result['avg_stay']
                avg_labs = result['avg_lab_procedures']
                
                print(f"   {readmission_status} patients:")
                print(f"     Count: {count:,}")
                print(f"     Avg Medications: {avg_meds:.1f}")
                print(f"     Avg Hospital Stay: {avg_stay:.1f} days")
                print(f"     Avg Lab Procedures: {avg_labs:.1f}")
                print()
            
            return results
            
        except Exception as e:
            print(f"❌ Error in readmission analysis: {e}")
            return []
    
    def analyze_medication_impact(self):
        """Analyze how medication count affects readmission"""
        print("\n💊 Analyzing medication impact on readmission...")
        
        try:
            pipeline = [
                {"$bucket": {
                    "groupBy": "$num_medications",
                    "boundaries": [0, 5, 10, 15, 20, 100],
                    "default": "20+",
                    "output": {
                        "total_patients": {"$sum": 1},
                        "readmitted_count": {
                            "$sum": {
                                "$cond": [
                                    {"$in": ["$readmitted", ["YES", ">30"]]}, 
                                    1, 
                                    0
                                ]
                            }
                        },
                        "avg_stay": {"$avg": "$time_in_hospital"}
                    }
                }},
                {"$sort": {"_id": 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            print("📈 Medication Impact Analysis:")
            for result in results:
                med_range = result['_id']
                total = result['total_patients']
                readmitted = result['readmitted_count']
                readmission_rate = (readmitted / total) * 100 if total > 0 else 0
                avg_stay = result['avg_stay']
                
                print(f"   {med_range} medications:")
                print(f"     Patients: {total:,}")
                print(f"     Readmission rate: {readmission_rate:.1f}%")
                print(f"     Avg stay: {avg_stay:.1f} days")
                print()
            
            return results
            
        except Exception as e:
            print(f"❌ Error in medication analysis: {e}")
            return []
    
    def age_group_analysis(self):
        """Analyze readmission patterns by age group"""
        print("\n👴 Analyzing age group patterns...")
        
        try:
            pipeline = [
                {"$group": {
                    "_id": "$age",
                    "total_patients": {"$sum": 1},
                    "readmission_rate": {
                        "$avg": {
                            "$cond": [
                                {"$in": ["$readmitted", ["YES", ">30"]]}, 
                                1, 
                                0
                            ]
                        }
                    },
                    "avg_medications": {"$avg": "$num_medications"},
                    "avg_stay": {"$avg": "$time_in_hospital"}
                }},
                {"$sort": {"_id": 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            print("📊 Age Group Analysis:")
            for result in results:
                age_group = result['_id']
                total = result['total_patients']
                readmission_rate = result['readmission_rate'] * 100
                avg_meds = result['avg_medications']
                avg_stay = result['avg_stay']
                
                print(f"   {age_group}:")
                print(f"     Patients: {total:,}")
                print(f"     Readmission rate: {readmission_rate:.1f}%")
                print(f"     Avg medications: {avg_meds:.1f}")
                print(f"     Avg stay: {avg_stay:.1f} days")
                print()
            
            return results
            
        except Exception as e:
            print(f"❌ Error in age analysis: {e}")
            return []
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("=" * 60)
        print("📋 DIABETES DATA ANALYSIS SUMMARY REPORT")
        print("=" * 60)
        
        # Get basic statistics
        total_patients = self.collection.count_documents({})
        print(f"Total patients analyzed: {total_patients:,}")
        
        # Run all analyses
        self.predict_readmission_risk()
        self.analyze_medication_impact() 
        self.age_group_analysis()
        
        print("=" * 60)
        print("✅ Analysis complete!")

# Simple test function
def main():
    """Test the advanced analysis"""
    analyzer = AdvancedDiabetesAnalysis()
    analyzer.generate_summary_report()

if __name__ == "__main__":
    main()