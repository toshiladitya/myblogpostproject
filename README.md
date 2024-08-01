# Blog Application

A simple Django-based blog application that allows users to create, view, filter, and share blog posts. This project includes functionalities such as user authentication, tagging, comments, and email sharing.

## Features

- **User Authentication**: Signup, login, and logout functionalities.
- **Blog Management**: Create, read, and filter blog posts.
- **Tagging**: Filter blog posts by tags.
- **Comments**: Add and like comments on blog posts.
- **Email Sharing**: Share blog posts via email.
- **Pagination**: Display 5 blogs per page.

## Requirements

- Python 3.x
- Django 5.x
- SQLite (for database)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/toshiladitya/myblogpostproject.git
   cd myblogpostproject
Set Up a Virtual Environment

bash
Copy code
python -m venv env
Activate the Virtual Environment
On Windows:

env\Scripts\activate
On macOS/Linux:

bash
Copy code
source env/bin/activate
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Apply Migrations

bash
Copy code
python manage.py migrate
Run the Development Server

bash
Copy code
python manage.py runserver
Open http://127.0.0.1:8000/ in your web browser to access the application.
