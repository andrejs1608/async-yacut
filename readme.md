# YaCut

**Foodgram is a service for publishing recipes and automatically generating shopping lists.**

## Key features

- Generate short links and link them to the original long links
- Redirect to the original address when accessing short links

## Technology stack

- Python 3.10
- Flask 2.0
- Jinja2 3.0
- SQLAlchemy 1.4

### How to run the Yacut project:

Clone the repository and navigate to it on the command line:

```
git clone
```

```
cd yacut
```

Create and activate a virtual environment:

```
python3 -m venv venv
```

* If you're on Linux/macOS

```
source venv/bin/activate
```

* If you're on Windows

```
source venv/scripts/activate
```

Install dependencies from the requirements.txt file:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Create a .env file with four variables in the project directory Environment:

```
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DB=sqlite:///db.sqlite3
```

Create a database and apply migrations:

```
flask db upgrade
```

Запустить проект:

```
flask run
```
