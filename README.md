# Student Database - Flask App

A simple web app for managing university student data. Built with Flask and MySQL.

## Setup

1. Clone the repo and go into the folder:
```
cd Student_DB
```

2. Install the dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file in the root folder with your database credentials:
```
DB_HOST=dbdev.cs.kent.edu
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_dbname
SECRET_KEY=whatever-you-want-here
```

4. If your database is empty, run the setup script to create the tables and load sample data:
```
python setup_db.py
```
You only need to do this once.

## Running the app locally

```
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000`

> Note: the app connects to a remote MySQL server so you need internet/VPN access to campus if running from off campus.

## Features

- Search students by name or ID (partial matches work)
- View each student's full course schedule
- Filter the schedule by year
- Add new students with a department dropdown
- Transfer students can have an initial credit count set
