# Academic Note
A web-based Academic Note Management System developed using Django. The system allows students to manage their academic courses, notes, and personal profiles in a secure and organized environment.

# Features

## Authentication
- User Registration
- User Login
- User Logout
- Email Verification
- Password Reset
- CAPTCHA Protection

## User Profile
- View Profile
- Edit Profile
- Upload Profile Picture
- Delete Account Verification

## Notes Management
- Create Notes
- Edit Notes
- Delete Notes
- View Note Details
- Organize Notes by Course

## Additional Pages
- Home Page
- About Us
- Contact Us
- login and signup
- course and note


# Technologies Used

- Python 3
- Django
- HTML
- CSS
- Javascript
- Docker
- Docker Compose



# Project Structure

academic_note/
│
├── academic_note/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── captcha.py
│   ├── email_verification.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
│
├── notes/
│   ├── migrations/
│   ├── static/
│   │   ├── images/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .dockerignore
├── .gitattributes
├── .gitignore
├── db.sqlite3
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
└── requirements.txt


# App
## Accounts

Responsible for user authentication and account management.

Includes:

- Login
- Registration
- Email Verification
- Password Reset
- CAPTCHA
- Profile Management


## Notes

Responsible for academic note management.

Includes:

- Course Management
- Note Creation
- Note Editing
- Note Details
- Profile Pages
- Contact Us
- About Us



# Installation

Clone the repository

```bash
git clone https://github.com/your-username/academic_note.git
```

Enter the project folder

```bash
cd academic_note
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Run the development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

# Running with Docker

Build and run the project

```bash
docker-compose up --build
```



# Running Tests

```bash
python manage.py test
```

Current test module:

```
accounts/tests.py
notes/tests.py
```


# Author

Arya and Paria  =>
Computer Science Student