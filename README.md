# [Stockmood]

[Stockmood] is a Flask application that visualizes stock sentiment using heat map, word cloud, bar charts, and emotional dot 
graphs etc. 

<br />

> Description

We are building our application using a Flask Dashboard boilerplate called Flask Dashboard Black (https://appseed.us/admin-dashboards/flask-dashboard-black).

We are using the following packages in our flask (v2.0.1) application:
- Flask_login (v0.5.0): provides user session management.
- Flask_migrate (v3.1.0): handles SQLAlchemy database migrations for flask.
- Flask_wtf (v0.15.1): used for designing forms in the flask web application.
- WTForms (v2.3.3): form rendering library.
- Flask_sqlalchemy (v2.5.1): an extension that supports SQLAlchemy with flask application.
- Sqlalchemy (v1.4.23): SQL toolkit and object-relational mapper for Python.
- Email_validator (v1.1.3): used for validating user email addresses during the signup process.
- Python-decouple (v3.4): helps separate our app settings from source code.
- Gunicorn (v20.1.0): Python web server gateway interface HTTP server.
- Jinja2 (v3.0.1): template rendering engine that renders our UI.
- Flask-restx (v0.5.1): flask extension for building REST APIs.
- Pandas (v1.3.4): used for transforming sql data to dataframe that passed to the front end.
- Nltk (v3.6.5): NLP library to preprocess text data for our ML models.
- Wordcloud (v1.6.0): used for creating visual representation of words based on its frequency of appearance.
- Numpy (v1.21.0): provides mathematical functions to help with transforming sql data.
- Matplotlib (v3.1.2): provides visualizations tools for some of our graphs.

<br />

> Data Downloading

Since the data is large, we stored it in a Google drive. The link is:https://drive.google.com/file/d/1Uug-_etcT_kd9vBLzqN6G1QULWy-GW5-/view?usp=sharing
Please download it and put it under apps file.


<br />

> Installation

```bash
$ # Unzip our team018final folder, and in the command prompt navigate to the code/stockmood directory
$ cd 202112-29-StockMood
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
```
<br />

> Execution

```bash
$ # In the command prompt, navigate to the project directory and run the following commands.
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ # (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
$
$
```

<br />

> Presentation and Demo Video

https://youtu.be/a7khBKCv8Ao
