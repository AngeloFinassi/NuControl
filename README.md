## **NuControl**
A web app built with Flask that allows users to upload bank statements for data visualization in table format and view categorized income and expense charts.

## Features
-User registration and login

-Upload files in different formats (csv, xlsx, xls, tsv, json)

-Separate storage per user

-Database with user and spreadsheet data

-Table data visualization

-Dashboard with charts based on the spreadsheet

-Delete files from the system

## Expected Spreadsheet Format
The spreadsheet must follow this exact format for the dashboard to work properly, as the spreadsheet-backend interaction was based on a model.

| data       | descrição  | valor   |
| ---------- | ---------- | ------- |
| 2025-05-10 | iFood      | -35.90  |
| 2025-05-10 | Company X  | 3000.00 |
| 2025-05-11 | Uber       | -12.50  |


Notes:

The column names must be exactly as shown above (no accents).

Negative values represent expenses, and positive values represent income.

Files other than .csv are read and saved as csv.

## Project Images
Upload Screen:
![image](https://github.com/user-attachments/assets/6e717f32-77b1-47df-906d-1776720d1d1a)


Dashboard:
![image](https://github.com/user-attachments/assets/ff0a5bb8-a615-4e31-8690-805cd2e2223c)


## Technologies Used
-Python 3.10+

-Flask

-Flask-Session

-SQLite3

-Pandas / Numpy

-Chart.js

-Jinja2

-HTML/CSS

## How to Run Locally
Clone the repository:

`https://github.com/AngeloFinassi/NuControl`

Enter the project folder:

`cd NuControl`

Install dependencies (use a virtualenv if you like):

`pip install -r requirements.txt`

Start the server (Flask's local server):

`python app.py`

Access the app at: http://127.0.0.1:5000

## Requirements
-Python 3.10+

-Browser

-Spreadsheet in the correct format!

## Security
Passwords are saved using hash (generate_password_hash).

Uploads are organized by user and saved with secure names.

Only authenticated users can view their files and dashboard.

There is no SQL injection in the web app inputs, all queries are formatted following security standards.
