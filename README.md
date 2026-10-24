# Employee Registration App

A Flask + MySQL employee registration app with Bootstrap, required-field validation, employee listing, and deletion.

## Requirements
- Python 3.10+
- MySQL Server
- Git (for GitHub submission)

## Setup
1. Create and activate a virtual environment:
   - Windows: `py -m venv .venv`
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - Command Prompt: `.\.venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run `schema.sql` in MySQL Workbench or the MySQL command line.
4. Set your MySQL password:
   - PowerShell: `$env:DB_PASSWORD="your_actual_mysql_password"`
   - Command Prompt: `set DB_PASSWORD=your_actual_mysql_password`
   - Or replace `YOUR_MYSQL_PASSWORD` in `app.py` for a local assessment only. Never commit real passwords.
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000`

## Features
- Register employee with name, email, department, and phone.
- Browser-side and server-side validation.
- Store data in MySQL using parameterized SQL.
- View employees in a Bootstrap table.
- Delete employee records.
- Prevent duplicate email addresses.

## Database
The schema is in `schema.sql`.

## GitHub
Do not upload passwords or secret keys. Upload the source code, schema, README, and requirements file.
