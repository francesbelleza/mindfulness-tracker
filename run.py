# Created by Frances Belleza -  Mindfulness Tracker
#
# File: app/ run.py
# Function: This file is used just to run

from app import app
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

if __name__ == "__main__":
    app.run(debug=True)