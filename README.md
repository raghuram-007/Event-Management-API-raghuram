
# Event Management API

A RESTful Event Management System built using Django and Django REST Framework (DRF).
The API allows users to create events, RSVP, and leave reviews.
It demonstrates use of serializers, viewsets, permissions, and JWT authentication.

# Features
## 🧩 Core Functionality

User Profiles with extended fields (full name, bio, location, profile picture)

Events: Create, update, delete, and list events

RSVPs: Mark attendance status for events (Going, Maybe, Not Going)

Reviews: Add and view event reviews

## 🔐 Authentication & Permissions

JWT Authentication (via djangorestframework-simplejwt)

Only event organizers can edit or delete their events

Private events visible only to invited users (custom permission)

## 🧭 Extra Features (Optional)

Pagination for events and reviews

Filtering and search by title, location, or organizer

Unit tests for endpoints## Author

👤 **Author:** Raghu Ram  
🌐 **GitHub:** [raghuram-007](https://github.com/raghuram-007)  



![Author](https://img.shields.io/badge/Author-Raghu%20Ram-blue?style=for-the-badge)
![GitHub](https://img.shields.io/badge/GitHub-raghuram--007-black?style=for-the-badge&logo=github&logoColor=white)
# 🗓️ Event Management API

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-API-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-yellow?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Postman](https://img.shields.io/badge/Tested%20With-Postman-orange?logo=postman&logoColor=white)](https://www.postman.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
# Tech Stack

| Component              | Technology                          |
| ---------------------- | ----------------------------------- |
| Backend Framework      | Django 5.x                          |
| API Framework          | Django REST Framework               |
| Authentication         | JWT (via SimpleJWT)                 |
| Database               | SQLite (default) / MySQL (optional) |                      |
| Testing                | Django TestCase / DRF APITestCase   |

## ⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/raghuram-007/Event-Management-API-raghuram.git

cd EventManagementAPI

## 2️⃣ Create & Activate Virtual Environment
python -m venv venv

venv\Scripts\activate          # For Windows

## 3️⃣ Install Dependencies
pip install -r requirements.txt


# 🧱 Database Setup

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

# ▶️ Run the Server
python manage.py runserver


The server will start at http://127.0.0.1:8000/
# 🧩 API Endpoints

## 🔸 Event API

| Method | Endpoint            | Description                   | Auth Required |
| ------ | ------------------- | ----------------------------- | ------------- |
| POST   | `/api/events/`      | Create a new event            | ✅ Yes         |
| GET    | `/api/events/`      | List all public events        | ❌ No          |
| GET    | `/api/events/{id}/` | Get event details             | ❌ No          |
| PUT    | `/api/events/{id}/` | Update event (organizer only) | ✅ Yes         |
| DELETE | `/api/events/{id}/` | Delete event (organizer only) | ✅ Yes         |

## 🔸 RSVP API

| Method | Endpoint                                 | Description        | Auth Required |
| ------ | ---------------------------------------- | ------------------ | ------------- |
| POST   | `/api/events/{event_id}/rsvp/`           | RSVP to an event   | ✅ Yes         |
| PATCH  | `/api/events/{event_id}/rsvp/{user_id}/` | Update RSVP status | ✅ Yes         |

## 🔸 Review API

| Method | Endpoint                          | Description                | Auth Required |
| ------ | --------------------------------- | -------------------------- | ------------- |
| POST   | `/api/events/{event_id}/reviews/` | Add review to event        | ✅ Yes         |
| GET    | `/api/events/{event_id}/reviews/` | List all reviews for event | ❌ No          |

# 🔑 JWT Authentication

Use the following endpoints for JWT authentication:

| Endpoint              | Description                      |
| --------------------- | -------------------------------- |
| `/api/token/`         | Obtain access and refresh tokens |
| `/api/token/refresh/` | Refresh access token             |

# 🧪 Running Tests

python manage.py test

## Runserver
python manage.py runserver
