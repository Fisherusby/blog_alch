# Blog with SQLAlchemy

## I. Tech stack

- Flask
- Flask-WTForms
- Flask-Bootstrap4
- SQLAlchemy

## II. Quick install

### 1. Clone project

```commandline
git clone https://github.com/Fisherusby/blog_alch.git
```
### 2. Install requirements packages

```commandline
pip install -r requirements
```

### 3. Init database

```commandline
python setup.py
```

### 4. Run app

```commandline
flask --app core run
```
or with debug
```commandline
flask --app core run --debug
``` 
### 5. Use app

Link for use app http://localhost:5000/

## III. Settings

Use environment variable:

- SECRET_KEY
- SQLALCHEMY_DATABASE_URI