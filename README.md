# FastAPI Shop App

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-009688?style=for-the-badge&logo=fastapi)
![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?style=for-the-badge&logo=vue.js)
![Docker](https://img.shields.io/badge/Docker-Dockerized-2496ED?style=for-the-badge&logo=docker)
![API](https://img.shields.io/badge/API-REST-orange?style=for-the-badge)

</div>

## About this project

A full-stack e-commerce web application with authentication, product management, and order system.

## 🚀 Features

### 🛍️ Shop

- View products
- Product details page
- Add products to cart
- Dynamic cart management

### 📦 Orders

- Create orders
- View user orders
- Order details page

### 👤 Authentication

- JWT-based authentication
- User registration & login
- Role-based access (Admin/User)

### 🛠️ Admin Panel

- Create / update / delete products
- Manage catalog

### 🖼️ Media

- Product images
- Profile pictures

### ⚙️ Backend

- REST API with FastAPI
- Async database support
- Redis caching
- Structured project architecture

---

## 🏗️ Project Structure

```bash
backend/ # FastAPI application
frontend/ # Vue 3 client
nginx/ # Reverse proxy configuration
docker-compose.yml
```

## 📚 API Documentation

### Authentication

| Method | Endpoint    | Description                                                |
| ------ | ----------- | ---------------------------------------------------------- |
| POST   | `/register` | Register a new user                                        |
| POST   | `/login`    | Login with username/password (returns JWT + refresh token) |
| POST   | `/refresh`  | Refresh access token using refresh token cookie            |
| POST   | `/logout`   | Logout and invalidate refresh token                        |

### Admin

#### Products

| Method | Endpoint                       | Description                           |
| ------ | ------------------------------ | ------------------------------------- |
| POST   | `/admin/products`              | Add a new product (with image upload) |
| PATCH  | `/admin/products/{product_id}` | Update product info                   |
| DELETE | `/admin/products/{product_id}` | Remove product                        |

#### Categories

| Method | Endpoint                        | Description      |
| ------ | ------------------------------- | ---------------- |
| POST   | `/admin/categories`               | Add new category |
| DELETE | `/admin/categories/{category_id}` | Delete category  |

#### Orders

| Method | Endpoint                   | Description         |
| ------ | -------------------------- | ------------------- |
| GET    | `/admin/orders`            | List all orders     |
| GET    | `/admin/orders/{order_id}` | Get order details   |
| PATCH  | `/admin/orders/{order_id}` | Update order status |

#### Users

| Method | Endpoint                 | Description                                 |
| ------ | ------------------------ | ------------------------------------------- |
| GET    | `/admin/users`           | List all users (limit/offset)               |
| GET    | `/admin/users/{user_id}` | Get user info                               |
| PATCH  | `/admin/users/{user_id}` | Update user role (returns new access token) |

### Products

| Method | Endpoint                 | Description                                 |
| ------ | ------------------------ | ------------------------------------------- |
| GET    | `/products`              | List products, Optional query parameters for filtering and pagination.                                                                       |
| GET    | `/products/{product_id}`|Get single product details                    |

### Category

| Method | Endpoint                 | Description                                 |
| ------ | ------------------------ | ------------------------------------------- |
| GET    | `/categories`            | List all categories                         |

### Orders

| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| POST   | `/orders`            | Place a new order          |
| GET    | `/orders`            | List current user's orders |
| DELETE | `/orders/{order_id}` | Delete order (user)        |

### Cart

| Method | Endpoint              | Description                               |
| ------ | --------------------- | ----------------------------------------- |
| GET    | `/items`              | Get current user cart                     |
| POST   | `/items`              | Add item to cart                          |
| DELETE | `/items/{product_id}` | Remove item from cart (optional quantity) |
| DELETE | `/items`              | Clear entire cart                         |

### Profile

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| PATCH  | `/profile`       | Update username / password |
| PATCH  | `/profile/image` | Update profile image       |

### OAuth 2.0 (Google)

| Method | Endpoint           | Description                  |
| ------ | ------------------ | ---------------------------- |
| GET    | `/google/url`      | Get Google OAuth URL         |
| POST   | `/google/callback` | Handle Google OAuth callback |

### User

| Method | Endpoint           | Description                  |
| ------ | ------------------ | ---------------------------- |
| GET    | `/users/me`        | Get current user info        |

## Technologies Used

### Backend

- **FastAPI**
- **SQLAlchemy (Async ORM)**
- **PostgreSQL / SQLite**
- **redis**
- **alembic**
- **Pydantic**
- **PyJWT**
- **passlib**
- **python-multipart**
- **httpx**
- **aiofiles**
- **Uvicorn**

### Frontend

- **Vue 3**
- **Vue Router**
- **Vite**
- **Tailwind CSS**
- **Axios**

### DevOps

- **Docker**
- **Docker Compose**
- **Nginx (Reverse Proxy)**

## ⚙️ Local Installation

### Prerequisites

- Python 3.11+ (for backend development)
- Node.js (for frontend development)
- Redis Server (required for local backend development)
- Git
- Docker (recommended)

### Environment Variables

Create a backend .env file:

```bash
cd backend

type nul > .env # For Widnows
# or
touch .env # For Linux/Mac
```

fill it in with the following variables:

```env
SECRET_KEY="Secret_Key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL="database_url"
REDIS_URL="redis://redis:6379"

STATIC_FOLDER="static"
PROFILE_PICTURES_PATH="static/profile_pictures"
DEFAULT_PROFILE_PICTURE_URL="static/default_profile_pic/default.png"
PRODUCT_IMAGES_PATH="static/product_images"

FRONTEND_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]
REDIRECT_URI="http://localhost:5173/"

OAUTH_GOOGLE_CLIENT_ID="Google ID"
OAUTH_GOOGLE_CLIENT_SECRET="Google Secret"

DEBUG_MODE=true
```

## 🐳 Running with Docker (Recommended)

**Make sure Docker is installed and running**

```bash
docker-compose up --build
```

## 💻 Running Locally (Development)

Make sure your local redis server is running.

### Backend

```bash
cd backend
python -m venv venv

venv/Scripts/activate   # Windows
source venv/bin/activate # Linux/Mac

pip install -r requirements.txt

python run.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access the application

- Frontend (Vue + Vite): http://localhost:5173
- Backend (FastAPI): http://localhost:8000

## 🧪 Testing

### Install the dependencies

```bash
cd backend
pip install -r requirements-test.txt
```

### Run the tests

```bash
cd backend
pytest -v
```

### Run a specific file

```bash
cd backend
pytest -v tests/test_auth.py
```
