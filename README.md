# Fastapi Maktabkhooneh - Expense Manager

A modern and efficient expense management API built with **FastAPI**, designed as a practice project for the FastAPI course held by [Ali Bigdeli](https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B7%D8%B1%D8%A7%D8%AD%DB%8C-%D8%B3%D8%B1%D9%88%DB%8C%D8%B3-fastapi-mk10645/). This service demonstrates best practices in building scalable REST APIs with authentication, database migrations, caching, and error tracking.

## Features

- **User Authentication**: Secure user registration and login with JWT tokens
- **Token Refresh**: Automatic access token refresh using refresh tokens  
- **Expense Management**: Create, read, update, and delete personal expenses
- **Multilingual Support**: Built-in support for English and Persian (Farsi) languages
- **Caching**: Redis-based caching for improved performance
- **Error Tracking**: Integrated Sentry for error monitoring and reporting
- **Database Migrations**: Alembic-based database versioning
- **Docker Support**: Complete Docker and Docker Compose setup for easy deployment
- **Load Testing**: Locust configuration for performance testing
- **Security**: Password hashing with Argon2, HTTP-only secure cookies

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI server
- **Database**: PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) ORM
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Caching**: [Redis](https://redis.io/)
- **Authentication**: JWT with [PyJWT](https://pyjwt.readthedocs.io/)
- **Password Security**: [Argon2-CFFI](https://argon2-cffi.readthedocs.io/)
- **Internationalization**: Python-based message translation
- **Error Tracking**: [Sentry](https://sentry.io/)
- **Testing**: [Pytest](https://pytest.org/)
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.14+
- PostgreSQL 16+
- Redis 8.6+
- Docker & Docker Compose (optional, for containerized setup)
- pip or uv package manager

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fastapi-maktabkhooneh.git
cd fastapi-maktabkhooneh
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or using uv (if available):
```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/maktabkhooneh

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-change-this-in-production
JWT_ACCESS_TOKEN_DUR=300  # 5 minutes in seconds
JWT_REFRESH_TOKEN_DUR=25200  # 7 hours in seconds
AUTH_COOKIE_SECURE=True

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Sentry Configuration (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456

# Supported Languages
SUPPORTED_LANGUAGES=["fa", "en"]
DEFAULT_LANGUAGE=en
```

### 5. Initialize Database

```bash
# Run migrations
alembic upgrade head
```

## Docker Setup

### Using Docker Compose

The easiest way to get started with all services:

```bash
# Development environment
docker-compose -f docker-compose.yml up -d

# Production environment
docker-compose -f docker-compose.prod.yml up -d
```

This will start:
- PostgreSQL database
- Redis cache
- FastAPI backend

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000/api/v1`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Health Checks

- **Readiness Check**: `GET /api/v1/is-ready`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/register` | Register a new user |
| POST | `/api/v1/users/login` | Login and receive tokens |
| POST | `/api/v1/users/refresh` | Refresh access token |
| POST | `/api/v1/users/logout` | Logout and clear cookies |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/expenses` | Get all expenses (paginated) |
| GET | `/api/v1/expenses/{expense_id}` | Get a specific expense |
| POST | `/api/v1/expenses` | Create a new expense |
| PUT | `/api/v1/expenses/{expense_id}` | Update an expense |
| DELETE | `/api/v1/expenses/{expense_id}` | Delete an expense |

### Authentication

All expense endpoints require authentication via JWT token in cookies or headers.

## Database Schema

### Users Table
- `id` (int, PK): User identifier
- `username` (string): Unique username
- `password` (string): Hashed password
- `is_active` (bool): Account status
- `created_date` (datetime): Account creation timestamp
- `updated_date` (datetime): Last update timestamp

### Expenses Table
- `id` (int, PK): Expense identifier
- `amount` (int): Expense amount (must be positive)
- `description` (string): Expense description
- `created_date` (datetime): Creation timestamp
- `updated_date` (datetime): Last update timestamp
- `user_id` (int, FK): Associated user ID

## Project Structure

```
.
├── main.py                 # Application entry point
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Development Docker setup
├── docker-compose.prod.yml # Production Docker setup
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project metadata
├── entrypoint.sh         # Docker entrypoint script
├── dockerfiles/          # Docker images
│   ├── Dockerfile        # Production image
│   └── Dockerfile.dev    # Development image
├── src/
│   ├── auth.py          # JWT token generation and verification
│   ├── configs.py       # Configuration management
│   ├── database.py      # Database session management
│   ├── exceptions.py    # Custom exceptions
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── utils.py         # Utility functions
│   ├── routes/          # API route handlers
│   │   ├── users.py     # User authentication routes
│   │   └── expenses.py  # Expense management routes
│   ├── locales/         # Internationalization
│   │   ├── en/          # English translations
│   │   └── fa/          # Persian translations
│   └── tests/           # Tests (optional)
├── migrations/          # Alembic migration files
└── locust/             # Load testing scripts
```

## Testing

Run tests with pytest:

```bash
pytest -v
pytest --cov=src  # With coverage report
```

For load testing with Locust:

```bash
locust -f locust/locustfile.py --host=http://localhost:8000
```

## Security Considerations

- **Password Hashing**: Uses Argon2 for secure password hashing
- **JWT Tokens**: Short-lived access tokens (5 minutes) and longer-lived refresh tokens
- **HTTP-Only Cookies**: Tokens stored in secure, HTTP-only cookies
- **CORS**: Configure as needed for your frontend
- **Environment Variables**: Keep sensitive data in `.env` files (never commit to version control)
- **Production Settings**: Set `AUTH_COOKIE_SECURE=True` in production

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///:memory:` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | Development key |
| `JWT_ACCESS_TOKEN_DUR` | Access token lifetime (seconds) | 300 |
| `JWT_REFRESH_TOKEN_DUR` | Refresh token lifetime (seconds) | 25200 |
| `AUTH_COOKIE_SECURE` | Use secure cookies in production | True |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SENTRY_DSN` | Sentry error tracking DSN | Empty (optional) |
| `SUPPORTED_LANGUAGES` | List of supported languages | `["fa", "en"]` |
| `DEFAULT_LANGUAGE` | Default language code | `"en"` |

## Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback to previous migration:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

## Error Handling

The application includes comprehensive error handling:

- **404 Not Found**: When expenses or users don't exist
- **409 Conflict**: When attempting to register with existing username
- **401 Unauthorized**: When authentication fails or token is invalid
- **422 Unprocessable Entity**: When request validation fails

Error messages support multiple languages based on the `Accept-Language` header.

## Internationalization (i18n)

The project supports multiple languages through translation files in `src/locales/`:

- **English**: `src/locales/en/LC_MESSAGES/`
- **Persian (Farsi)**: `src/locales/fa/LC_MESSAGES/`

Language is determined by the `Accept-Language` header in requests.

## Performance

- **Caching**: Redis integration for caching frequent queries
- **Pagination**: Expense list endpoint supports limit/offset pagination
- **Connection Pooling**: SQLAlchemy handles database connection pooling


## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ArmanMehr/fastapi-maktabkhooneh/blob/main/LICENCE) file for details.

## Acknowledgments

This project is part of the FastAPI course practices created by [Ali Bigdeli](https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B7%D8%B1%D8%A7%D8%AD%DB%8C-%D8%B3%D8%B1%D9%88%DB%8C%D8%B3-fastapi-mk10645/). Special thanks for the comprehensive learning materials and best practices demonstrated throughout the course.
