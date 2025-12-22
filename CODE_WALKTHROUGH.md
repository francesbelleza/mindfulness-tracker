# Code Walkthrough - Mindfulness Tracker App

**Author:** Frances Belleza
**Last Updated:** December 22, 2025
**Purpose:** Comprehensive guide explaining every function, class, and component in the recalibrate mindfulness tracker application.

---

## Table of Contents
1. [Project Architecture Overview](#project-architecture-overview)
2. [Application Entry Point](#application-entry-point)
3. [Application Factory & Initialization](#application-factory--initialization)
4. [Configuration Management](#configuration-management)
5. [Database Models](#database-models)
6. [Routes & Application Logic](#routes--application-logic)
7. [Templates](#templates)
8. [Database Migrations](#database-migrations)
9. [Static Assets](#static-assets)
10. [Environment Variables](#environment-variables)

---

## Project Architecture Overview

This is a Flask-based web application following the **Application Factory Pattern**. The project structure:

```
mindfulness-tracker/
├── run.py                          # Application entry point
├── app/
│   ├── __init__.py                # App factory & Flask extensions
│   ├── config.py                  # Configuration class
│   ├── models.py                  # Database models (SQLAlchemy)
│   ├── mindfulness_tracker_app.py # Route handlers
│   ├── templates/                 # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── login_required.html
│   └── static/
│       └── styles.css             # Custom CSS
├── migrations/                     # Alembic database migrations
│   └── versions/
│       ├── 7c20b258252c_initial_database_schema.py
│       └── 8a31c96f4d2e_add_user_model.py
├── .env                           # Environment variables (gitignored)
├── requirements.txt               # Python dependencies
└── docs/                          # Project documentation
```

**Key Design Patterns:**
- **Application Factory:** Flask app created via `create_app()` function
- **Blueprints (Future):** Currently using route registration pattern, can migrate to blueprints
- **MVC-like:** Models (models.py), Views (templates/), Controllers (routes)

---

## Application Entry Point

### File: `run.py`

**Purpose:** Entry point for running the Flask application.

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

**Explanation:**

#### Import Statement
```python
from app import create_app
```
- Imports the `create_app` factory function from the `app` package (defined in `app/__init__.py`)

#### App Instantiation
```python
app = create_app()
```
- Calls the factory function to create and configure a Flask application instance
- This returns a fully configured Flask app with all extensions initialized

#### Development Server
```python
if __name__ == "__main__":
    app.run(debug=True)
```
- **`if __name__ == "__main__"`:** Ensures this code only runs when the file is executed directly (not imported)
- **`app.run(debug=True)`:** Starts Flask's built-in development server
  - `debug=True` enables:
    - Auto-reload when code changes
    - Detailed error pages with stack traces
    - Interactive debugger in browser
  - **⚠️ WARNING:** Never use `debug=True` in production!

**How to Run:**
```bash
python run.py
# OR
flask run
```

---

## Application Factory & Initialization

### File: `app/__init__.py`

**Purpose:** Creates and configures the Flask application with all extensions and settings.

#### Global Extension Objects

```python
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
```

**Why create these globally?**
- Extensions are initialized without an app instance first
- Later bound to the app in `create_app()` via `init_app()`
- Allows the same extensions to be imported across multiple modules
- Prevents circular import issues

---

#### Function: `create_app()`

**Purpose:** Application factory function that creates and configures a Flask app instance.

```python
def create_app():
    # 1. Create Flask app instance
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # 2. Load configuration
    app.config.from_object(Config)

    # 3. Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # 4. Register routes
    with app.app_context():
        from app import mindfulness_tracker_app
        mindfulness_tracker_app.initial_routes(app)

    return app
```

**Step-by-Step Breakdown:**

##### 1. Create Flask Instance
```python
app = Flask(__name__, static_folder='static', template_folder='templates')
```
- **`__name__`:** Tells Flask where to find resources (current package name)
- **`static_folder='static'`:** Directory for CSS, JS, images (serves at `/static/`)
- **`template_folder='templates'`:** Directory for Jinja2 HTML templates

##### 2. Load Configuration
```python
app.config.from_object(Config)
```
- Loads all configuration variables from the `Config` class in `config.py`
- Sets `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, etc.

##### 3. Initialize Extensions
```python
db.init_app(app)
```
- Binds SQLAlchemy database to this Flask app
- Enables database operations like `db.session.add()`, `db.session.commit()`

```python
migrate.init_app(app, db)
```
- Initializes Flask-Migrate (Alembic wrapper)
- Enables migration commands: `flask db migrate`, `flask db upgrade`

```python
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
```
- **`login_manager.init_app(app)`:** Binds Flask-Login to app
- **`login_view = 'login'`:** Redirect destination for unauthorized users
- **`login_message_category = 'info'`:** Bootstrap alert class for flash messages

##### 4. Register Routes
```python
with app.app_context():
    from app import mindfulness_tracker_app
    mindfulness_tracker_app.initial_routes(app)
```
- **`app.app_context()`:** Creates an application context for route registration
- Imports the routes module and calls `initial_routes(app)` to register all routes
- Routes are registered as decorators (`@app.route()`)

---

#### Function: `load_user(user_id)`

**Purpose:** Flask-Login callback to reload the user object from the user ID stored in the session.

```python
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
```

**How it Works:**
1. **Decorator `@login_manager.user_loader`:** Registers this function with Flask-Login
2. **Called on every request** when a user is logged in
3. **`user_id`:** The ID stored in the Flask session (as a string)
4. **`int(user_id)`:** Converts string to integer for database query
5. **`User.query.get()`:** Retrieves User object by primary key
6. **Returns:** User object or `None` (if user doesn't exist)

**Why is this needed?**
- Flask-Login stores only the user ID in the session (not the whole object)
- This callback fetches the full User object so `current_user` works in templates/routes

---

#### Unauthorized Handler Configuration

```python
login_manager.login_view = 'login'
login_manager.login_message = None
login_manager.unauthorized_handler(lambda: (render_template('login_required.html'), 401))
```

**Line-by-Line:**

```python
login_manager.login_view = 'login'
```
- Sets the route name to redirect to when `@login_required` fails
- In this case, redirects to the `/login` route

```python
login_manager.login_message = None
```
- Disables Flask-Login's default flash message ("Please log in to access this page")
- You're handling the message via a custom template instead

```python
login_manager.unauthorized_handler(lambda: (render_template('login_required.html'), 401))
```
- **Purpose:** Customizes what happens when unauthorized users access protected routes
- **Lambda function:** Returns a tuple `(response, status_code)`
  - `render_template('login_required.html')`: Shows custom unauthorized page
  - `401`: HTTP status code for "Unauthorized"
- **Why?** Provides better UX with a friendly message instead of just redirecting

---

## Configuration Management

### File: `app/config.py`

**Purpose:** Centralized configuration loaded from environment variables.

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**Explanation:**

#### Load Environment Variables
```python
from dotenv import load_dotenv
load_dotenv()
```
- **`python-dotenv`:** Library that loads variables from `.env` file into `os.environ`
- **`load_dotenv()`:** Reads `.env` in project root and makes variables accessible via `os.getenv()`

#### Configuration Class
```python
class Config:
```
- Flask can load config from objects (classes)
- All uppercase attributes become config variables

#### Configuration Variables

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```
- **Purpose:** Used by Flask for session encryption and CSRF protection
- **Security:** Should be a long random string
- **Current Value:** `recalibrate-yo-$h1t` (should be changed for production!)

```python
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
```
- **Purpose:** Database connection string
- **Format:** `postgresql://user:password@host:port/database`
- **Current:** Points to Render.com hosted PostgreSQL database

```python
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
- **Purpose:** Disables SQLAlchemy event system that tracks object modifications
- **Why False?** Saves memory and reduces overhead
- **Recommended:** Always set to `False` unless you specifically need modification tracking

---

## Database Models

### File: `app/models.py`

**Purpose:** Defines database tables as Python classes using SQLAlchemy ORM.

---

### Class: `User`

**Purpose:** Represents a registered user in the application.

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### Class Inheritance

```python
class User(UserMixin, db.Model):
```

**`db.Model`:**
- Base class from SQLAlchemy
- Makes this class a database table
- Table name: `user` (lowercase class name by default)

**`UserMixin`:**
- From Flask-Login
- Provides default implementations for:
  - `is_authenticated`: Returns `True` if user is logged in
  - `is_active`: Returns `True` if account is active
  - `is_anonymous`: Returns `False` for real users
  - `get_id()`: Returns user ID as a string

#### Database Columns

```python
id = db.Column(db.Integer, primary_key=True)
```
- **Type:** Integer
- **Primary Key:** Auto-increments, uniquely identifies each user
- **Usage:** Used in foreign keys, session storage

```python
username = db.Column(db.String(20), unique=True, nullable=False)
```
- **Type:** String (max 20 characters)
- **unique=True:** No two users can have the same username (database constraint)
- **nullable=False:** Required field, cannot be empty

```python
email = db.Column(db.String(120), unique=True, nullable=False)
```
- **Type:** String (max 120 characters)
- **unique=True:** Prevents duplicate emails
- **Usage:** Used for login authentication

```python
password_hash = db.Column(db.String(128), nullable=False)
```
- **Type:** String (128 characters)
- **Purpose:** Stores hashed password (NOT plain text!)
- **Security:** Uses Werkzeug's password hashing (bcrypt-like)

```python
created_at = db.Column(db.DateTime, default=datetime.utcnow)
```
- **Type:** DateTime
- **default=datetime.utcnow:** Automatically sets to current UTC time when user is created
- **Note:** `utcnow` is passed as a function reference (no parentheses!)

---

#### Method: `set_password(password)`

**Purpose:** Hashes and stores a user's password securely.

```python
def set_password(self, password):
    self.password_hash = generate_password_hash(password)
```

**How it Works:**
1. **Input:** Plain text password (string)
2. **`generate_password_hash(password)`:**
   - From `werkzeug.security`
   - Creates a salted hash using PBKDF2-SHA256
   - Output format: `method$salt$hash`
3. **Stores hash in `self.password_hash`** (never stores plain text!)

**Example Usage:**
```python
user = User(username='frances', email='frances@example.com')
user.set_password('mypassword123')  # Hashes and stores
db.session.add(user)
db.session.commit()
```

**Security Notes:**
- **Salted:** Each hash has a unique random salt
- **One-way:** Cannot reverse the hash to get original password
- **Slow:** Intentionally computationally expensive to prevent brute force

---

#### Method: `check_password(password)`

**Purpose:** Verifies if a provided password matches the stored hash.

```python
def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

**How it Works:**
1. **Input:** Plain text password attempt (string)
2. **`check_password_hash(hash, password)`:**
   - Extracts salt from stored hash
   - Hashes the input password with the same salt
   - Compares the two hashes
3. **Returns:** `True` if match, `False` otherwise

**Example Usage:**
```python
user = User.query.filter_by(email='frances@example.com').first()
if user and user.check_password('mypassword123'):
    print("Login successful!")
else:
    print("Invalid credentials")
```

**Why Not Use `==` to compare?**
- Timing attacks: `==` comparison time varies based on where strings differ
- `check_password_hash()` uses constant-time comparison to prevent timing attacks

---

### Commented Out: `TestModel`

```python
'''--------| TEST SPRINT 0 | DATABASE CONFIGS | ---------
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))
----------------------------------------------------- '''
```

**Purpose:**
- Used in Sprint 0 to test database connection to Render PostgreSQL
- Can be deleted once User model is migrated successfully
- Initial migration still references this model

---

## Routes & Application Logic

### File: `app/mindfulness_tracker_app.py`

**Purpose:** Defines all application routes (URL endpoints) and their handler functions.

---

### Function: `initial_routes(app)`

**Purpose:** Wrapper function that registers all route handlers with the Flask app.

```python
def initial_routes(app):
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        # ... route logic ...
```

**Why wrap routes in a function?**
- Allows route registration to happen inside `create_app()` with application context
- Prevents circular imports
- All routes share the same `app` instance

---

### Route: `/signup`

**Purpose:** User registration page and form handler.

```python
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # ----- TODO: add validation (unique, email format, length) ----
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')
```

**Step-by-Step Breakdown:**

#### Route Decorator
```python
@app.route('/signup', methods=['GET', 'POST'])
```
- **URL:** `/signup`
- **Methods:**
  - `GET`: Show signup form (default page load)
  - `POST`: Process form submission

#### Check If User Already Logged In
```python
if current_user.is_authenticated:
    return redirect(url_for('index'))
```
- **`current_user`:** Flask-Login proxy object representing the logged-in user
- **`.is_authenticated`:** Property from `UserMixin`, returns `True` if logged in
- **Purpose:** Prevent logged-in users from accessing signup page
- **Redirects to:** Home page (`index`)

#### Handle Form Submission (POST)
```python
if request.method == 'POST':
```
- **`request`:** Flask global object containing HTTP request data
- **`.method`:** HTTP method (`GET`, `POST`, etc.)

##### Extract Form Data
```python
username = request.form['username']
email = request.form['email']
password = request.form['password']
```
- **`request.form`:** Dictionary-like object containing POST data
- **Keys match `name` attributes** in HTML form inputs
- **⚠️ TODO:** Add validation (see TODO comment)

**Missing Validations:**
- Username/email uniqueness check (will currently cause database error)
- Email format validation
- Password length requirements
- XSS/injection protection (basic protection via Jinja2 auto-escaping)

##### Create User Object
```python
user = User(username=username, email=email)
user.set_password(password)
```
1. Creates new `User` instance with username and email
2. Calls `set_password()` to hash password and store in `password_hash`

##### Save to Database
```python
db.session.add(user)
db.session.commit()
```
- **`db.session.add(user)`:** Stages user object for insertion
- **`db.session.commit()`:** Executes SQL INSERT statement
- **⚠️ Can fail if:** Username/email already exists (unique constraint)

##### Flash Success Message
```python
flash('Account created successfully! Please log in.', 'success')
```
- **`flash()`:** Stores a message in session to display on next request
- **First arg:** Message text
- **Second arg:** Category (`success`, `danger`, `info`, `warning`) - maps to Bootstrap alert classes

##### Redirect to Login
```python
return redirect(url_for('login'))
```
- **`url_for('login')`:** Generates URL for `login` route (e.g., `/login`)
- **`redirect()`:** HTTP 302 redirect response

#### Show Signup Form (GET)
```python
return render_template('signup.html')
```
- **`render_template()`:** Processes Jinja2 template and returns HTML
- Displays when page is first loaded or if form validation fails (future implementation)

---

### Route: `/login`

**Purpose:** User login page and authentication handler.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')
```

**Step-by-Step Breakdown:**

#### Prevent Double Login
```python
if current_user.is_authenticated:
    return redirect(url_for('index'))
```
- Same logic as signup - already logged-in users redirected to home

#### Handle Login Form (POST)

##### Get Credentials
```python
email = request.form['email']
password = request.form['password']
```
- Extracts email and password from form

##### Query User
```python
user = User.query.filter_by(email=email).first()
```
- **`User.query`:** SQLAlchemy query object for User table
- **`.filter_by(email=email)`:** Filters WHERE email = 'value'
- **`.first()`:** Returns first match or `None` if not found

##### Verify Credentials
```python
if user and user.check_password(password):
```
- **`user`:** Checks if user exists (not `None`)
- **`user.check_password(password)`:** Verifies password hash matches

##### Log In User
```python
login_user(user)
```
- **`login_user()`:** Flask-Login function
- **What it does:**
  1. Stores user ID in Flask session
  2. Sets `current_user` to this User object
  3. Updates last login time (if configured)
- **Session persists** across requests (cookie-based)

##### Handle "Next" Parameter
```python
next_page = request.args.get('next')
return redirect(next_page) if next_page else redirect(url_for('index'))
```

**What is `next`?**
- When `@login_required` blocks a user, Flask-Login adds `?next=/protected-page` to login URL
- After login, user is redirected back to where they were trying to go

**Example Flow:**
1. User tries to access `/check-in` (protected)
2. Redirected to `/login?next=/check-in`
3. After successful login, redirected to `/check-in`

**Security Note:**
- **⚠️ Open Redirect Vulnerability:** Should validate `next` parameter to prevent redirects to external sites
- **Fix:** Check if `next` starts with `/` or use `url_parse(next).netloc == ''`

##### Handle Failed Login
```python
flash('Login failed. Check your email and password.', 'danger')
```
- Shows error message if credentials are invalid
- **Category:** `danger` (red Bootstrap alert)

**Security Best Practice:**
- Generic message ("Check your email and password") prevents username enumeration
- Doesn't reveal whether email exists in database

#### Show Login Form (GET)
```python
return render_template('login.html')
```
- Displays login form template

---

### Route: `/logout`

**Purpose:** Logs out the current user and ends their session.

```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
```

**Step-by-Step Breakdown:**

#### Protect Route
```python
@login_required
```
- **Decorator from Flask-Login**
- **Purpose:** Only logged-in users can access this route
- **If not logged in:** Redirects to `login_manager.login_view` (the `/login` route)

#### Log Out User
```python
logout_user()
```
- **`logout_user()`:** Flask-Login function
- **What it does:**
  1. Removes user ID from session
  2. Sets `current_user` to `AnonymousUserMixin` instance
  3. Clears session cookie

#### Flash Message
```python
flash('You have been logged out.', 'info')
```
- Confirms logout to user
- **Category:** `info` (blue Bootstrap alert)

#### Redirect to Home
```python
return redirect(url_for('index'))
```
- Sends user to public home page

---

### Route: `/check-in`

**Purpose:** Placeholder route for daily mood check-in (to be implemented in Sprint 2).

```python
@app.route('/check-in')
@login_required
def check_in():
    return render_template('check_in.html')
```

**Current State:**
- Protected by `@login_required`
- Currently just renders a template (stub)
- **Sprint 2 TODO:** Implement check-in form and logic

**Planned Functionality (Sprint 2):**
- Display mood selection form
- Check if user already checked in today
- Save check-in to database
- Redirect to practice suggestions

---

### Route: `/` (Index)

**Purpose:** Home page / landing page.

```python
@app.route('/')
def index():
    return render_template('index.html')
```

**Simple Route:**
- No authentication required (public page)
- Just renders the home page template
- Template shows "Start Check-In" button

---

## Templates

All templates use **Jinja2** templating engine and extend a base template for consistency.

---

### Template: `base.html`

**Purpose:** Master template containing common layout elements (navbar, flash messages, footer, etc.).

#### Key Components:

##### HTML Head
```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}recalibrate{% endblock %}</title>

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
```

**Explanation:**
- **`<meta charset="utf-8">`:** Character encoding (supports emojis, international characters)
- **`<meta name="viewport">`:** Makes site mobile-responsive
- **`{% block title %}`:** Jinja2 block that child templates can override
- **Bootstrap CDN:** Loads Bootstrap 5.3.2 CSS framework
- **`{{ url_for('static', filename='styles.css') }}`:** Generates URL for custom CSS

**Jinja2 Syntax:**
- **`{% ... %}`:** Logic/control structures (if, for, block, etc.)
- **`{{ ... }}`:** Output/expression (prints value)

##### Navigation Bar
```html
<nav class="navbar navbar-expand-lg navbar-light bg-white mb-4">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{{ url_for('index') }}" style="color: #C3521A;">
      recalibrate
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto">
        {% if current_user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
          </li>
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('signup') }}">Sign Up</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

**Conditional Navigation:**
```jinja2
{% if current_user.is_authenticated %}
  <!-- Show Logout link -->
{% else %}
  <!-- Show Login/Sign Up links -->
{% endif %}
```

- **`current_user.is_authenticated`:** True if user is logged in
- **Dynamic menu:** Changes based on auth state
- **Mobile-responsive:** Hamburger menu on small screens

##### Flash Messages
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <div class="mb-4">
      {% for category, msg in messages %}
        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
          {{ msg }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endfor %}
    </div>
  {% endif %}
{% endwith %}
```

**How Flash Messages Work:**

1. **`get_flashed_messages(with_categories=true)`:**
   - Retrieves all messages stored via `flash()`
   - Returns list of tuples: `[('success', 'Account created!'), ...]`

2. **Loop through messages:**
   - **`category`:** Bootstrap alert class (`success`, `danger`, `info`, `warning`)
   - **`msg`:** The message text

3. **Bootstrap Alerts:**
   - **`alert-{{ category }}`:** Dynamic class (e.g., `alert-success` = green)
   - **`alert-dismissible`:** Adds close button
   - **`fade show`:** Fade-in animation

**Example Output:**
```html
<div class="alert alert-success alert-dismissible fade show">
  Account created successfully!
  <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

##### Content Block
```html
<div class="container">
  {% block content %}{% endblock %}
</div>
```

- **`{% block content %}`:** Placeholder where child templates inject their content
- **`<div class="container">`:** Bootstrap container for centered, responsive layout

##### JavaScript
```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```
- Loads Bootstrap JavaScript (needed for navbar toggle, alerts, etc.)

---

### Template: `index.html`

**Purpose:** Landing page / home page.

```html
{% extends "base.html" %}
{% block title %}Welcome{% endblock %}

{% block content %}
  <div class="text-center py-5">
    <h1 class="display-4">welcome to recalibrate</h1>
    <p class="lead">Take a moment to check in with yourself.</p>
    <a href="{{ url_for('check_in') }}" class="btn btn-primary btn-lg mt-4">
      Start Check-In
    </a>
  </div>
{% endblock %}
```

**Explanation:**

- **`{% extends "base.html" %}`:** Inherits layout from base template
- **`{% block title %}`:** Overrides page title
- **`{% block content %}`:** Replaces content block with this HTML

**Bootstrap Classes:**
- **`text-center`:** Centers all text
- **`py-5`:** Padding (vertical) - spacing
- **`display-4`:** Large heading style
- **`lead`:** Larger paragraph text
- **`btn btn-primary btn-lg`:** Large blue button

**Call to Action:**
- "Start Check-In" button links to `/check-in` route
- If not logged in → redirected to login page (due to `@login_required`)

---

### Template: `signup.html`

**Purpose:** User registration form.

```html
{% extends "base.html" %}
{% block title %}Sign Up{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-md-6 col-lg-5">
    <h2 class="mb-4 text-center">Create an Account</h2>
    <form method="POST" class="needs-validation" novalidate>
      <!-- username, email, password fields... -->
      <button type="submit" class="btn btn-primary w-100">Create Account</button>
    </form>
    <p class="mt-3 text-center">
      Already have an account? <a href="{{ url_for('login') }}">Log In</a>
    </p>
  </div>
</div>
{% endblock %}
```

**Form Attributes:**
- **`method="POST"`:** Submits data via POST request
- **`class="needs-validation"`:** Bootstrap validation class
- **`novalidate`:** Disables browser validation (use Bootstrap's instead)

**Note:** The actual form fields are abbreviated in the file (comment says `<!-- username, email, password fields... -->`). In a complete implementation, these would include:

```html
<div class="mb-3">
  <label class="form-label">Username</label>
  <input type="text" name="username" class="form-control" required>
</div>
<div class="mb-3">
  <label class="form-label">Email</label>
  <input type="email" name="email" class="form-control" required>
</div>
<div class="mb-3">
  <label class="form-label">Password</label>
  <input type="password" name="password" class="form-control" required>
</div>
```

**Layout:**
- **`row justify-content-center`:** Centers form horizontally
- **`col-md-6 col-lg-5`:** Responsive width (50% on medium screens, 42% on large)

---

### Template: `login.html`

**Purpose:** User login form.

```html
{% extends "base.html" %}
{% block title %}Log In{% endblock %}

{% block content %}
  <h2 class="mb-4 text-center" style="color:#C3521A;">Log In</h2>
  <form method="POST" action="{{ url_for('login') }}" class="mx-auto" style="max-width:360px;">
    <div class="mb-3">
      <label class="form-label">Email</label>
      <input type="email" name="email" class="form-control" placeholder="you@example.com" required>
    </div>
    <div class="mb-3">
      <label class="form-label">Password</label>
      <input type="password" name="password" class="form-control" placeholder="••••••" required>
    </div>
    <button type="submit" class="btn btn-primary w-100">Log In</button>
  </form>
{% endblock %}
```

**Form Details:**

```html
<form method="POST" action="{{ url_for('login') }}" class="mx-auto" style="max-width:360px;">
```
- **`method="POST"`:** ✅ FIXED! (was missing before)
- **`action="{{ url_for('login') }}"`:** Submits to `/login` route
- **`mx-auto`:** Centers form horizontally
- **`max-width:360px`:** Narrow form width

**Input Fields:**

```html
<input type="email" name="email" class="form-control" placeholder="you@example.com" required>
```
- **`type="email"`:** HTML5 email validation
- **`name="email"`:** ✅ FIXED! Key for `request.form['email']`
- **`required`:** Browser-level validation

```html
<input type="password" name="password" class="form-control" placeholder="••••••" required>
```
- **`type="password"`:** Masks input
- **`name="password"`:** ✅ FIXED! Key for `request.form['password']`

**Submit Button:**
```html
<button type="submit" class="btn btn-primary w-100">Log In</button>
```
- **`type="submit"`:** ✅ FIXED! (explicit submit type)
- **`w-100`:** Full width button

---

### Template: `login_required.html`

**Purpose:** Custom 401 Unauthorized page shown when non-authenticated users try to access protected routes.

```html
{% extends "base.html" %}
{% block title %}Login Required{% endblock %}

{% block content %}
<div class="alert alert-warning mt-5 text-center">
  Please <a href="{{ url_for('login') }}">log in</a> to access this page.
</div>
{% endblock %}
```

**How It's Triggered:**
```python
login_manager.unauthorized_handler(lambda: (render_template('login_required.html'), 401))
```

**Instead of:**
- Redirecting to login
- Showing a flash message

**You get:**
- Custom page with friendly message
- HTTP 401 status code
- Link to login page

---

## Database Migrations

**Purpose:** Version control for database schema changes.

### File: `migrations/versions/7c20b258252c_initial_database_schema.py`

**What it does:**
- Creates `test_model` table with `id` and `message` columns
- Part of Sprint 0 database connection testing

```python
def upgrade():
    op.create_table('test_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('test_model')
```

- **`upgrade()`:** Applied when running `flask db upgrade`
- **`downgrade()`:** Reverts changes when running `flask db downgrade`

---

### File: `migrations/versions/8a31c96f4d2e_add_user_model.py`

**What it does:**
- Creates `user` table with all User model columns
- **Status:** Migration file created, but not yet applied to database

```python
def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
```

**Constraints:**
- **Primary Key:** `id`
- **Unique Constraints:** `username` and `email`
- **NOT NULL:** `username`, `email`, `password_hash`

**To Apply Migration:**
```bash
source venv/bin/activate
flask db upgrade
```

**Migration Chain:**
```
None → 7c20b258252c (test_model) → 8a31c96f4d2e (user)
```

---

## Static Assets

### File: `app/static/styles.css`

**Purpose:** Custom CSS overrides and branding.

**Key Customizations:**
- **Brand Color:** `#C3521A` (burnt orange)
- **Button Styling:** Primary buttons use brand color
- **Link Colors:** Burnt orange theme
- **Typography:** Tahoma font family

**Example:**
```css
.btn-primary {
    background-color: #C3521A !important;
    border-color: #C3521A !important;
}

a {
    color: #C3521A;
}
```

**Bootstrap Override:**
- Uses `!important` to override Bootstrap's default blue theme

---

## Environment Variables

### File: `.env`

**⚠️ THIS FILE IS GITIGNORED - Never commit to version control!**

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://mindfulness_tracker_data_user:0gCUKxexssAczIq5YuxvNr7srjl0ug88@dpg-d0bcu19r0fns73dbgcmg-a.oregon-postgres.render.com/mindfulness_tracker_data
SECRET_KEY=recalibrate-yo-$h1t
OPENAI_API_KEY=your-api-key-here
```

**Variable Explanations:**

#### `FLASK_APP=run.py`
- Tells Flask which file to run when using `flask run` command
- Points to entry point file

#### `FLASK_ENV=development`
- Sets environment mode
- **development:** Auto-reload, debug mode, detailed errors
- **production:** Optimizations, no auto-reload, generic errors

#### `DATABASE_URL`
- PostgreSQL connection string for Render.com hosted database
- **Format:** `postgresql://username:password@host:port/database`
- **⚠️ Security:** Contains credentials - must keep secret!

#### `SECRET_KEY`
- Used by Flask for:
  - Session encryption
  - CSRF token generation
  - Cookie signing
- **⚠️ TODO:** Change to a stronger random key for production
- **Generate secure key:**
  ```python
  import secrets
  secrets.token_hex(32)
  ```

#### `OPENAI_API_KEY`
- Placeholder for Sprint 3 AI integration
- **Current:** Not yet used
- **Future:** Will power AI mindfulness suggestions and journal prompts

---

## Summary: What Each File Does

| File | Purpose | Key Functions/Classes |
|------|---------|----------------------|
| `run.py` | Application entry point | Runs Flask dev server |
| `app/__init__.py` | App factory & config | `create_app()`, `load_user()` |
| `app/config.py` | Configuration management | `Config` class |
| `app/models.py` | Database models | `User` class, `set_password()`, `check_password()` |
| `app/mindfulness_tracker_app.py` | Routes & logic | `signup()`, `login()`, `logout()`, `check_in()`, `index()` |
| `app/templates/base.html` | Master template | Navbar, flash messages, layout |
| `app/templates/index.html` | Home page | Welcome message, CTA button |
| `app/templates/signup.html` | Registration form | User signup form |
| `app/templates/login.html` | Login form | User login form |
| `app/templates/login_required.html` | 401 error page | Unauthorized access message |
| `app/static/styles.css` | Custom styling | Burnt-orange brand theme |
| `migrations/versions/*.py` | Database migrations | Schema version control |

---

## Next Steps: Sprint 2 Implementation

Based on `PLANNING.md`, here's what needs to be built:

### 1. CheckIn Model
Create in `app/models.py`:
```python
class CheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(20), nullable=False)  # Happy, Calm, Anxious, Sad
    body_feeling = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    user = db.relationship('User', backref='checkins')
```

### 2. Update `/check-in` Route
Add logic to:
- Check if user already checked in today
- Display mood selection form (emoji-based)
- Save check-in to database
- Redirect to `/practice` (Sprint 3 placeholder)

### 3. Create Templates
- `check_in.html` - Mood selector form
- `already_checked_in.html` - Friendly duplicate check-in message

### 4. Database Migration
```bash
flask db migrate -m "add checkin model"
flask db upgrade
```

---

## Tips for Working with This Codebase

### Running the App
```bash
source venv/bin/activate
python run.py
# OR
flask run
```

### Database Migrations
```bash
# Create a migration after model changes
flask db migrate -m "description of changes"

# Apply migrations
flask db upgrade

# Revert last migration
flask db downgrade
```

### Flask Shell (Interactive Testing)
```bash
flask shell

>>> from app.models import User
>>> user = User(username='test', email='test@example.com')
>>> user.set_password('password123')
>>> db.session.add(user)
>>> db.session.commit()
```

### Common Issues

**Issue:** `flask: command not found`
**Fix:** Activate virtual environment first

**Issue:** Database connection errors
**Fix:** Check if Render database is active (free tier may pause)

**Issue:** Changes not showing
**Fix:** Hard refresh browser (Cmd+Shift+R) or clear cache

---

**End of Code Walkthrough**
*Last Updated: December 22, 2025*
