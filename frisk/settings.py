import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(APP_DIR, 'app.db')