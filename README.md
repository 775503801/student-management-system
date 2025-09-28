# Student Management System (Flask + SQLite)

A simple, ready-to-run Student Management web app built with Flask and SQLite.
Designed to be easy to understand and deploy. 

## Features
- Add / Edit / Delete students
- List students with basic search
- Simple responsive UI using vanilla HTML/CSS/JS
- SQLite database (file-based)

## Requirements
- Python 3.8+
- pip

## Setup (local)
1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd student-management-system
   ```
2. Create a virtual environment (recommended) and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate    # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Initialize the database and run the app:
   ```
   flask --app app --debug run
   ```
   Open http://127.0.0.1:5000 in your browser.

## Files
- `app.py` : Flask application and API routes.
- `templates/index.html` : Frontend (Jinja2).
- `static/css/style.css` : Basic styling.
- `static/js/app.js` : Frontend JS for interacting with the API.
- `students.db` : (created at runtime) SQLite DB file.


## License
MIT
