# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ run.py
# Function: This file is used just to run
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)