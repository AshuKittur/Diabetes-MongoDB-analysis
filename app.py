from flask import Flask, render_template_string, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls

# Embedded HTML template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diabetes Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #667eea;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }

        .stat-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .stat-icon {
            font-size: 2rem;
            margin-right: 10px;
        }

        .stat-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
        }

        .stat-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-description {
            color: #666;
            font-size: 0.9rem;
        }

        .chart-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }

        .chart-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }

        .readmission-bars {
            display: flex;
            align-items: end;
            justify-content: space-around;
            height: 200px;
            margin: 20px 0;
        }

        .bar {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 100px;
        }

        .bar-fill {
            width: 60px;
            border-radius: 8px 8px 0 0;
            margin-bottom: 10px;
            transition: all 0.5s ease;
            display: flex;
            align-items: end;
            justify-content: center;
            color: white;
            font-weight: bold;
            padding-bottom: 10px;
        }

        .bar-label {
            font-weight: 600;
            color: #333;
            text-align: center;
            line-height: 1.2;
        }

        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #c33;
            margin: 20px 0;
        }

        .footer {
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
            font-size: 0.9rem;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .readmission-bars {
                height: 150px;
            }
            
            .stat-value {
                font-size: 2rem;
            }
        }

        /* Loading animation */
        .loading-spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🏥 Diabetes Dashboard</h1>
            <p>Real-time Patient Analytics & Readmission Insights</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">👥</span>
                    <span class="stat-title">Total Patients</span>
                </div>
                <div class="stat-value" id="totalPatients">-</div>
                <div class="stat-description">Patients in database</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">🏨</span>
                    <span class="stat-title">Avg Hospital Stay</span>
                </div>
                <div class="stat-value" id="avgStay">-</div>
                <div class="stat-description">Days per admission</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">💊</span>
                    <span class="stat-title">Avg Medications</span>
                </div>
                <div class="stat-value" id="avgMeds">-</div>
                <div class="stat-description">Per patient visit</div>
            </div>

            <div class="stat-card">
                <div class="stat-header">
                    <span class="stat-icon">🧪</span>
                    <span class="stat-title">Avg Lab Tests</span>
                </div>
                <div class="stat-value" id="avgLabs">-</div>
                <div class="stat-description">Per patient visit</div>
            </div>
        </div>

        <div class="chart-container">
            <div class="chart-title">📊 Patient Readmission Analysis</div>
            <div id="readmissionChart">
                <div class="loading">
                    <div class="loading-spinner"></div>
                    Loading readmission data...
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Healthcare Analytics Dashboard • Real-time MongoDB Integration</p>
        </div>
    </div>

    <script>
        // API call to get statistics
        async function loadDashboardData() {
            try {
                const response = await fetch('/api/stats');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                // Update basic stats
                document.getElementById('totalPatients').textContent = data.total_patients?.toLocaleString() || '0';
                document.getElementById('avgStay').textContent = (data.averages?.avg_stay || 0) + ' days';
                document.getElementById('avgMeds').textContent = data.averages?.avg_meds || '0';
                document.getElementById('avgLabs').textContent = data.averages?.avg_labs || '0';
                
                // Create readmission chart
                createReadmissionChart(data.readmission_stats || []);
                
            } catch (error) {
                console.error('Error loading dashboard data:', error);
                showError('Failed to load dashboard data: ' + error.message);
            }
        }

        function createReadmissionChart(readmissionStats) {
            const chartContainer = document.getElementById('readmissionChart');
            
            if (!readmissionStats || readmissionStats.length === 0) {
                chartContainer.innerHTML = '<div class="error">No readmission data available</div>';
                return;
            }

            // Calculate total for percentages
            const total = readmissionStats.reduce((sum, item) => sum + item.count, 0);
            
            // Map readmission values to labels
            const readmissionLabels = {
                'NO': 'No Readmission',
                '<30': 'Within 30 Days',
                '>30': 'After 30 Days'
            };

            // Create bars HTML
            let barsHTML = '<div class="readmission-bars">';
            
            readmissionStats.forEach((item, index) => {
                const percentage = ((item.count / total) * 100).toFixed(1);
                const height = (item.count / Math.max(...readmissionStats.map(s => s.count))) * 150;
                const colors = ['#667eea', '#f093fb', '#4facfe'];
                const color = colors[index % colors.length];
                
                barsHTML += `
                    <div class="bar">
                        <div class="bar-fill" style="height: ${height}px; background: ${color};">
                            ${item.count}
                        </div>
                        <div class="bar-label">
                            ${readmissionLabels[item._id] || item._id}<br>
                            <small>${percentage}%</small>
                        </div>
                    </div>
                `;
            });
            
            barsHTML += '</div>';
            chartContainer.innerHTML = barsHTML;
        }

        function showError(message) {
            const chartContainer = document.getElementById('readmissionChart');
            chartContainer.innerHTML = `<div class="error">${message}</div>`;
            
            // Reset stats to show error state
            ['totalPatients', 'avgStay', 'avgMeds', 'avgLabs'].forEach(id => {
                document.getElementById(id).textContent = 'Error';
            });
        }

        // Load data when page loads
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardData();
            
            // Refresh data every 30 seconds
            setInterval(loadDashboardData, 30000);
        });

        // Test connection on page load
        fetch('/test')
            .then(response => response.json())
            .then(data => {
                console.log('Flask connection test:', data);
            })
            .catch(error => {
                console.error('Connection test failed:', error);
            });
    </script>
</body>
</html>
'''

# MongoDB connection with error handling
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client['diabetes_project']
    collection = db['patient_data']
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    collection = None

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def get_stats():
    """API endpoint for basic statistics"""
    try:
        if collection is None:
            return jsonify({"error": "Database connection not available"}), 500
            
        # Total patients
        total_patients = collection.count_documents({})
        
        # Readmission rates
        readmission_pipeline = [
            {"$group": {
                "_id": "$readmitted", 
                "count": {"$sum": 1}
            }}
        ]
        readmission_stats = list(collection.aggregate(readmission_pipeline))
        
        # Average metrics - with error handling for empty collection
        avg_pipeline = [
            {"$group": {
                "_id": None,
                "avg_stay": {"$avg": "$time_in_hospital"},
                "avg_meds": {"$avg": "$num_medications"},
                "avg_labs": {"$avg": "$num_lab_procedures"}
            }}
        ]
        avg_result = list(collection.aggregate(avg_pipeline))
        
        if avg_result:
            avg_stats = avg_result[0]
            averages = {
                "avg_stay": round(avg_stats.get('avg_stay', 0) or 0, 1),
                "avg_meds": round(avg_stats.get('avg_meds', 0) or 0, 1),
                "avg_labs": round(avg_stats.get('avg_labs', 0) or 0, 1)
            }
        else:
            averages = {
                "avg_stay": 0,
                "avg_meds": 0,
                "avg_labs": 0
            }
        
        return jsonify({
            "total_patients": total_patients,
            "readmission_stats": readmission_stats,
            "averages": averages
        })
        
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test')
def test():
    """Test endpoint to verify Flask is running"""
    return jsonify({"status": "Flask is running", "mongodb_connected": collection is not None})

if __name__ == '__main__':
    print("🚀 Starting Flask dashboard...")
    print("📊 Open http://localhost:5000 in your browser")
    print("🔍 Test API at http://localhost:5000/test")
    print("📈 Stats API at http://localhost:5000/api/stats")
    app.run(debug=True, host='0.0.0.0', port=5000)