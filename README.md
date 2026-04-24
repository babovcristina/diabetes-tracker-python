# diabetes-tracker-python
CLI-based Diabetes Tracker built with Python and SQLite, including data analysis and trends 
Description

This application is designed to help track and analyze diabetes-related health data.

It allows users to record daily measurements and monitor long-term indicators such as HbA1c and weight.
In addition to data storage, the application provides basic analysis and insights.

 Technologies Used

- Python
- SQLite (local database)
- SQL (SELECT, INSERT, UPDATE, DELETE)

 Features

🔹 Measurements (Daily Tracking)

- Add daily measurements (glucose, water intake, steps, carbs)
- Display all records
- Modify existing entries
- Delete records

🔹 HbA1c (Every 3 Months)

- Add HbA1c values
- Display history
- Modify records
- Delete records
- Automatic status classification:
  - Good control
  - Consult your doctor

🔹 Weight (Monthly Tracking)

- Add weight records
- Display history
- Modify entries
- Delete records

🔹 Analysis & Insights

The application includes basic data analysis:

- Average glucose
- Highest glucose value
- Glucose when carbs are high and steps are low
- HbA1c trend (last 2 values)
- Weight trend (last 2 values)

 How It Works

1. Data Storage

All data is stored locally using SQLite in three tables:

- "measurements"
- "hba1c"
- "weight"

2. Date Handling

Dates are stored as text in the format:

YYYY-MM-DD

This allows correct chronological sorting using SQL ("ORDER BY date").

3. Trend Detection

The application compares the last two records:

- HbA1c:
 
  - Increasing → warning
  - Decreasing → improvement

- Weight:
 
  - Increasing → alert
  - Decreasing → positive trend

4. Input Validation

- Numeric validation using "try/except"
- Prevents invalid values (e.g., negative inputs)
- Ensures stable program execution

  How to Run

1. Make sure Python is installed
2. Run the script:

python diabetes_tracker.py

3. Use the menu to navigate through features

  What I Learned

- Working with SQLite databases
- Using SQL queries inside Python
- Structuring applications with multiple features
- Input validation and error handling
- Implementing simple data analysis (averages, trends)
- Writing reusable and organized code


  Future Improvements

- Graphical user interface (Tkinter or web app)
- Advanced analytics (correlations, trends over time)
- Export data (CSV/Excel)
- User authentication
