# URL Shortener

A modern, secure, and feature-rich URL shortener built with FastAPI and SQLAlchemy.

You can see an exmaple of this working at: https://urlshortner-8f0bb70ad7fb.herokuapp.com/
## Features

- ✨ Modern and responsive UI built with Bootstrap 5
- 🚀 Fast asynchronous backend with FastAPI
- 🔒 Complete authentication system with JWT tokens
- 👤 User dashboard for managing URLs
- 🔑 Optional password protection for URLs
- 📝 Custom URL aliases support
- 🕒 URL expiration support
- 📊 Click tracking and analytics
- 🔄 Real-time URL validation
- 📋 One-click copy functionality
- 🎨 Modern glassmorphism design
- 🛡️ Rate limiting and security features

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: Async ORM for database operations
- **PostgreSQL**: Primary database
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **Passlib**: Password hashing with bcrypt
- **Python-Jose**: JWT token handling
- **SlowAPI**: Rate limiting

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Clean, modern JavaScript
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icon library

## Core Features

### User Management
- User registration and authentication
- JWT token-based session management
- Secure password hashing with bcrypt
- Protected routes and user-specific content

### URL Management
- Create shortened URLs with optional features:
  - Custom aliases
  - Password protection
  - Expiration dates
- User dashboard for managing URLs:
  - View all created URLs
  - Enable/disable URLs
  - Add/remove password protection
  - Delete URLs
- Copy shortened URLs with one click

### Security Features
- Password protection for URLs
- Rate limiting for API endpoints
- CORS protection
- HTTPS redirection in production
- SQL injection protection
- XSS protection
- Secure cookie handling

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

4. Create a `.env` file in the root directory:
   ```env
   ENVIRONMENT=development
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=urlshort
   DATABASE_USERNAME=postgres
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=180
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

### Authentication
- `POST /auth/register`: Register new user
- `POST /auth/login`: Login user
- `GET /auth/logout`: Logout user

### URL Management
- `POST /api/shorten`: Create shortened URL
  ```json
  {
    "target_url": "https://example.com",
    "custom_code": "optional-alias",
    "expires_at": "2024-12-31T23:59:59Z",
    "password": "optional-password"
  }
  ```

- `GET /api/{short_code}`: Redirect to target URL
- `PUT /api/urls/{url_id}/toggle`: Enable/disable URL
- `PUT /api/urls/{url_id}/password`: Update URL password
- `DELETE /api/urls/{url_id}`: Delete URL

### Dashboard
- `GET /dashboard`: User dashboard for URL management

## Security Considerations

### Password Protection
- URLs can be optionally protected with passwords
- Passwords are hashed using bcrypt
- Protected URLs show a password entry form before redirecting
- Failed password attempts are tracked

### URL Validation
- All URLs are validated before shortening
- Custom codes are sanitized to prevent injection attacks
- Expired URLs are automatically deactivated
- Rate limiting prevents abuse


