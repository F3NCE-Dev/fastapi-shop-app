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
- Structured project architecture

---

## 🏗️ Project Structure

```bash
backend/
frontend/
nginx/
docker-compose.yml
```

## Technologies Used

### Backend

- **FastAPI**
- **SQLAlchemy**
- **aiosqlite**
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

- Python 3.11+
- Node.js (for frontend development)
- Docker (recommended)

### Environment Variables

Create a .env file in the root directory:

```bash
echo "" > .env
```

## 🐳 Running with Docker (Recommended)

```bash
docker-compose up --build
```

## 💻 Running Locally (Development)

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
