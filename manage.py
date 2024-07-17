# manage.py
from flask_migrate import Migrate
from flask import Flask
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

# for auto detecting the changes
if __name__ == '__main__':
    app.run(debug=True)
