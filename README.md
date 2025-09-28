# Diabetes Patient Analytics Dashboard

[](https://www.python.org/downloads/)
[](https://www.mongodb.com/)
[](https://flask.palletsprojects.com/)

A web-based dashboard that provides real-time analytics and insights into a diabetic patient dataset. The application leverages a MongoDB backend to perform complex queries and data analysis, presenting the findings in an intuitive user interface.

## Dashboard Preview

## Features

  - **Real-time KPIs:** Displays key metrics such as Total Patients, Average Hospital Stay, Average Medications, and Average Lab Tests.
  - **Patient Readmission Analysis:** Visualizes the distribution of patient readmissions (No Readmission, Within 30 Days, After 30 Days).
  - **MongoDB Integration:** Utilizes MongoDB for efficient storage and retrieval of patient data, making it suitable for handling large and semi-structured datasets.
  - **Data-Driven Insights:** The backend scripts are designed to explore, analyze, and run specific queries on the dataset to extract meaningful information.

## Technology Stack

  - **Backend:** Python, Flask
  - **Database:** MongoDB
  - **Data Analysis:** PyMongo, Pandas (likely)
  - **Frontend:** HTML, CSS, JavaScript (likely with a charting library like Chart.js or D3.js)

## Project Structure

```
.
├── templates/              # HTML templates for the web interface
│   └── index.html
├── .gitignore              # Files to be ignored by Git
├── README.md               # You are here!
├── advanced_analysis.py    # Scripts for more complex data analysis tasks
├── analyze_data.py         # Core scripts for calculating KPIs and metrics
├── app.py                  # Main Flask application file (runs the web server)
├── explore_data.py         # Initial data exploration and cleaning scripts
├── requirements.txt        # Python dependencies for the project
└── specific_queries.py     # Scripts for running specific, targeted queries on the database
```

## Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

  - Python 3.9+
  - MongoDB Community Server installed and running.
  - Git

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2\. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

Install all the necessary Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4\. Set up the Database

You need to import your dataset (e.g., from a CSV or JSON file) into your local MongoDB instance.

Assuming you have a `diabetic_data.csv` file, you can use the `mongoimport` command:

```bash
mongoimport --db diabetes_db --collection patients --type csv --headerline --file path/to/your/diabetic_data.csv
```

  - `--db diabetes_db`: Specifies the database name.
  - `--collection patients`: Specifies the collection name.
  - `--file path/to/your/diabetic_data.csv`: The path to your dataset file.

*Note: You may need to update the database connection string in the Python scripts if your setup is different from the default (`mongodb://localhost:27017/`).*

### 5\. Run the Application

Execute the main Flask application file.

```bash
python app.py
```

The application will start, typically on `http://127.0.0.1:5000`.
<img width="1344" height="910" alt="Screenshot 2025-09-28 232654" src="https://github.com/user-attachments/assets/b24891b0-b65e-47c9-bb2e-fe37ce2079cf" />

## Usage

Once the application is running, open your web browser and navigate to [http://127.0.0.1:5000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000). The dashboard will load and display the analytics derived from the MongoDB database.
