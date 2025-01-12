# URL Shortener

A modern, fast, and simple URL shortener built with FastAPI and SQLAlchemy.

## Features

- ✨ Modern and responsive UI
- 🚀 Fast asynchronous backend with FastAPI
- 🔒 URL validation and sanitization
- 🔑 Password protection for URLs
- 📝 Custom URL aliases support
- 🕒 Optional URL expiration
- 📊 Click tracking
- 🎨 Bootstrap 5 for styling
- 🔄 Real-time URL validation
- 📋 One-click copy functionality

## Tech Stack

- **Backend**:
  - FastAPI (ASGI web framework)
  - SQLAlchemy (Async ORM)
  - PostgreSQL (Database)
  - Alembic (Database migrations)
  - Pydantic (Data validation)
  - Passlib (Password hashing)

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Bootstrap 5
  - Font Awesome icons

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```env
   ENVIRONMENT=development
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=urlshort
   DATABASE_USERNAME=postgres
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ORIGINS_PROD=https://your-domain.com
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## API Endpoints

### POST /api/shorten
Creates a shortened URL

Request body:
```json
{
  "target_url": "https://example.com",
  "custom_code": "optional-alias",     // optional
  "expires_at": "2024-12-31T23:59:59Z", // optional
  "password": "secret123"              // optional
}
```

Response:
```json
{
  "target_url": "https://example.com",
  "short_code": "abc123",
  "created_at": "2024-01-12T00:00:00Z",
  "is_active": true,
  "is_protected": true
}
```

### GET /api/{short_code}
Redirects to the target URL or displays password form if URL is protected

### POST /api/{short_code}/verify
Verifies password for protected URLs

Request body (form data):
```
password: "your-password"
```

Response:
- If password is correct: Redirects to target URL
- If password is incorrect: Returns to password form with error message

## Security Features

### Password Protection
- URLs can be optionally protected with a password
- Passwords are securely hashed using bcrypt
- Protected URLs show a password entry form before redirecting
- Failed password attempts are tracked in the logs

### URL Validation
- All URLs are validated before shortening
- Custom codes are sanitized to prevent injection attacks
- Expired URLs are automatically deactivated
- Click tracking provides usage analytics