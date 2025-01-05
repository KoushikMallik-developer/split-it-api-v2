# Splitzy - Expense Sharing Application Backend

Welcome to **Splitzy**, the backend for an expense-sharing application built using **Django Rest Framework (DRF)**.
Splitzy provides APIs to manage group expenses, track balances, and simplify splitting bills among friends, family, or
colleagues.

---

## Features

- User Authentication (Sign up, Login, Token-based Authentication)
- Create and Manage Groups
- Add and Split Expenses Among Group Members
- Track Balances (Who owes whom and how much)
- Settle Up Balances
- Comprehensive RESTful APIs

---

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8+
- Django 4.0+
- Django Rest Framework
- PostgreSQL

---

## Installation

### 1. Clone the Repository

```bash
$ git clone https://github.com/yourusername/splitzy.git
$ cd splitzy
```

### 2. Set Up a Virtual Environment

```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
$ pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and configure the following variables:

```
DB_NAME = ******
DB_USERNAME = ******
DB_PASSWORD = ******
DB_HOST = ******
DB_PORT = ******
REDIS_HOST = ******
ENCRYPTION_PASSWORD = ******
JWT_ENCRYPTION_PASSWORD = ******
DJANGO_SECRET_KEY = ******
EMAIL_HOST_USER = ******
EMAIL_HOST_PASSWORD = ******
DEBUG_MODE = ******
FRONTEND_BASE_URL = ******
ENVIRONMENT_SETTINGS = ******

```

### 5. Run Migrations

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### 6. Create a Superuser (Admin Account)

```bash
$ python manage.py createsuperuser
```

### 7. Start the Development Server

```bash
$ python manage.py runserver
```

---

## API Endpoints

### Authentication

| Method | Endpoint                       | Description           |
|--------|--------------------------------|-----------------------|
| POST   | `/auth/api/v2/create-users`    | Register a new user   |
| POST   | `/auth/api/v2/sign-in`         | Login and get a token |
| POST   | `/auth/api/v2/send-otp/`       | Send OTP              |
| POST   | `/auth/api/v2/verify-otp`      | Verify OTP            |
| POST   | `/auth/api/v2/update-password` | Update Password       |
| POST   | `/auth/api/v2/reset-password`  | Reset Password        |
| POST   | `/auth/api/v2/remove-user`     | Remove User           |

### Friends and friend requests

| Method | Endpoint                                      | Description                     |
|--------|-----------------------------------------------|---------------------------------|
| GET    | `/friends/api/v2/my-friends`                  | Get all friends                 |
| GET    | `/friends/api/v2/my-friend-requests`          | Get all friend Request          |
| GET    | `/friends/api/v2/my-sent-friend-requests`     | Get all sent friend Request     |
| GET    | `/friends/api/v2/my-received-friend-requests` | Get all received friend Request |
| POST   | `/friends/api/v2/send-friend-request`         | Send a friend request           |
| POST   | `/friends/api/v2/accept-friend`               | Accept friend request           |
| POST   | `/friends/api/v2/remove-friend`               | Remove a friend                 |
| POST   | `/friends/api/v2/remove-friend-request`       | Remove a pending friend request |

### Groups

| Method | Endpoint                   | Description               |
|--------|----------------------------|---------------------------|
| GET    | `/api/groups/`             | List all groups           |
| POST   | `groups/api/v2/add-group`  | Create a new group        |
| POST   | `groups/api/v2/add-member` | Add a new member in group |
| GET    | `/api/groups/{id}/`        | Retrieve a specific group |
| PUT    | `/api/groups/{id}/`        | Update group details      |
| DELETE | `/api/groups/{id}/`        | Delete a group            |

### Expenses

| Method | Endpoint              | Description                 |
|--------|-----------------------|-----------------------------|
| GET    | `/api/expenses/`      | List all expenses           |
| POST   | `/api/expenses/`      | Add a new expense           |
| GET    | `/api/expenses/{id}/` | Retrieve a specific expense |
| PUT    | `/api/expenses/{id}/` | Update an expense           |
| DELETE | `/api/expenses/{id}/` | Delete an expense           |

### Balances

| Method | Endpoint                | Description               |
|--------|-------------------------|---------------------------|
| GET    | `/api/balances/`        | View all balances         |
| POST   | `/api/balances/settle/` | Settle a specific balance |

---

## Development

### Run Tests

Run the test suite to ensure everything works as expected:

```bash
$ pytest
```

### Linting

Ensure code quality by running a Cleaner:

```bash
$ clean.bat
```

---

## Deployment

### Using Docker

1. Build the Docker image:

```bash
$ docker build -t splitzy-backend .
```

2. Run the Docker container:

```bash
$ docker run -p 8000:8000 splitzy-backend
```

### Using Gunicorn and Nginx (Production Setup)

1. Install Gunicorn:

```bash
$ pip install gunicorn
```

2. Run Gunicorn:

```bash
$ gunicorn splitzy.wsgi:application --bind 0.0.0.0:8000
```

3. Set up Nginx as a reverse proxy to forward traffic to Gunicorn.

---

## Folder Structure

```
.
├── splitzy/             # Django project folder
├── expenses/            # App for managing expenses
├── friends/             # App for managing friends and friend requests
├── groups/              # App for managing groups
├── users/               # App for user authentication
├── requirements.txt     # Python dependencies
├── manage.py            # Django management script
└── README.md            # Project documentation
```

---

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Thanks to the Django and Django Rest Framework teams for their amazing tools.
- Special thanks to contributors and testers.

---

Happy coding! 🎉
