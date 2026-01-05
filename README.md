<p align="center">
  <h1 align="center">🎓 Student Management System</h1>
  <p align="center">
    <strong>Full-stack web application for managing student records</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
    <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind"/>
  </p>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [API Endpoints](#api-endpoints)
  - [Data Crawler](#data-crawler--analysis)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Crawler & Data Analysis](#-crawler--data-analysis)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🌟 Overview

A comprehensive student management system built with modern technologies. The system provides:

- **RESTful API** returning XML responses
- **Beautiful UI** with React and Tailwind CSS
- **Data Analysis** capabilities with Pandas
- **Containerized** deployment with Docker Compose

### Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic | Python 3.11 |
| **Frontend** | React, Vite, Tailwind CSS | React 18 |
| **Database** | PostgreSQL | 16-alpine |
| **Container** | Docker Compose | v2 |
| **Data Analysis** | Pandas, OpenPyXL | Latest |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✅ **CRUD Operations** | Create, Read, Update, Delete students |
| ✅ **XML API** | All endpoints return `application/xml` |
| ✅ **Partial Data** | Students can have missing fields |
| ✅ **100 Sample Records** | Pre-seeded database on startup |
| ✅ **Beautiful UI** | Tailwind CSS + Headless UI |
| ✅ **Data Crawler** | Scrape & analyze data with Pandas |
| ✅ **Excel Export** | Export analysis to Excel file |
| ✅ **Docker Ready** | One command deployment |

---

## 🚀 Quick Start

Get up and running in **3 simple steps**:

```bash
# 1. Clone and navigate
cd PPR501-Final-Project

# 2. Create environment file
cp .env.example .env

# 3. Start all services
docker compose up --build -d
```

🎉 **Done!** Access the application:

| Service | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:3000 |
| 📖 API Docs | http://localhost:8000/docs |
| 📊 HTML Table | http://localhost:8000/students |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Download |
|-------------|---------|----------|
| Docker Desktop | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

> 📝 **Note**: Python is NOT required! The crawler runs via Docker.

---

## 🔧 Installation

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd PPR501-Final-Project

# Create environment configuration
cp .env.example .env

# Build and start all services
docker compose up --build -d

# View logs (optional)
docker compose logs -f
```

### Option 2: Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/students_db"

# Run server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

</details>

---

## 📖 Usage

### Web Interface

1. Open http://localhost:3000 in your browser
2. View the list of 100 pre-seeded students
3. **Add Student**: Fill the form and click "Thêm sinh viên"
4. **Edit Student**: Click on a row to select, modify form, click "Cập nhật"
5. **Delete Student**: Click delete icon, confirm in dialog

### API Endpoints

All endpoints return **XML** responses:

```bash
# Get all students
curl http://localhost:8000/api/students

# Get single student
curl http://localhost:8000/api/students/SV0001

# Create student
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{"student_id":"SV9999","last_name":"Nguyen","first_name":"Van A"}'

# Update student
curl -X PUT http://localhost:8000/api/students/SV9999 \
  -H "Content-Type: application/json" \
  -d '{"email":"updated@example.com"}'

# Delete student
curl -X DELETE http://localhost:8000/api/students/SV9999
```

### Data Crawler & Analysis

See [Crawler Section](#-crawler--data-analysis) for detailed instructions.

---

## 📁 Project Structure

```
PPR501-Final-Project/
│
├── 📂 backend/                 # FastAPI Backend Service
│   ├── 📂 app/
│   │   ├── 📂 api/v1/         # API routes (versioned)
│   │   │   └── endpoints/     # REST endpoints
│   │   ├── 📂 core/           # Config & database
│   │   ├── 📂 models/         # SQLAlchemy ORM models
│   │   ├── 📂 schemas/        # Pydantic validation
│   │   ├── 📂 services/       # Business logic layer
│   │   ├── 📂 utils/          # Utilities (XML, Pandas)
│   │   └── 📂 templates/      # HTML templates
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📂 frontend/                # React Frontend Service
│   ├── 📂 src/
│   │   ├── 📂 components/     # UI Components
│   │   │   ├── ui/           # Reusable (Button, Input, etc.)
│   │   │   ├── layout/       # Header, Footer
│   │   │   └── students/     # Student-specific
│   │   ├── 📂 hooks/         # Custom React hooks
│   │   ├── 📂 services/      # API service layer
│   │   ├── 📂 pages/         # Page components
│   │   └── 📂 utils/         # Helpers, XML parser
│   ├── Dockerfile
│   └── package.json
│
├── 📂 crawler/                 # Data Crawler & Analysis
│   ├── crawl_and_analyze.py   # Main crawler script
│   └── requirements.txt
│
├── 📂 docker/db/              # Database initialization
│   ├── init.sql              # Schema + seed script
│   └── students.csv          # 100 sample students
│
├── docker-compose.yml         # Container orchestration
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🏗 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
├─────────────────┬─────────────────────┬─────────────────────────┤
│                 │                     │                         │
│  ┌───────────┐  │  ┌───────────────┐  │  ┌─────────────────┐   │
│  │ Frontend  │  │  │    Backend    │  │  │   PostgreSQL    │   │
│  │  (React)  │──┼──│   (FastAPI)   │──┼──│   (Database)    │   │
│  │  :3000    │  │  │    :8000      │  │  │     :5432       │   │
│  └───────────┘  │  └───────────────┘  │  └─────────────────┘   │
│        │        │         │           │           │             │
│   Nginx Proxy   │    REST API         │     100 Students       │
│   /api/* ───────┼────────>│           │        Seeded          │
│                 │                     │                         │
└─────────────────┴─────────────────────┴─────────────────────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │      Crawler        │
                  │  (Python/Pandas)    │
                  │  Scrape & Analyze   │
                  └─────────────────────┘
```

### Backend Architecture (Clean Architecture)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │   API Endpoints (app/api/v1/endpoints/)                     │ │
│  │   - students.py: REST handlers returning XML                │ │
│  └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Business Layer                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │   Services (app/services/)                                  │ │
│  │   - student_service.py: CRUD logic, data transformation    │ │
│  └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Data Layer                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │   Models (app/models/)                                      │ │
│  │   - student.py: SQLAlchemy ORM entity                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                    Infrastructure                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │   Core (app/core/)                                          │ │
│  │   - config.py: Pydantic Settings                            │ │
│  │   - database.py: SQLAlchemy engine & session               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 API Reference

### Base URL

```
http://localhost:8000/api
```

### Endpoints

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/students` | List all students | XML array |
| `GET` | `/students/{id}` | Get single student | XML object |
| `POST` | `/students` | Create student | XML object (201) |
| `PUT` | `/students/{id}` | Update student | XML object |
| `DELETE` | `/students/{id}` | Delete student | Empty (204) |

### Student Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `student_id` | string | ✅ Yes | Unique identifier (e.g., SV0001) |
| `last_name` | string | ❌ No | Family name |
| `first_name` | string | ❌ No | Given name |
| `email` | string | ❌ No | Email address |
| `birth_date` | date | ❌ No | Date of birth (YYYY-MM-DD) |
| `hometown` | string | ❌ No | Place of origin |
| `math_score` | float | ❌ No | Math score (0-10) |
| `literature_score` | float | ❌ No | Literature score (0-10) |
| `english_score` | float | ❌ No | English score (0-10) |

### Example Response

```xml
<?xml version='1.0' encoding='utf-8'?>
<students>
  <student>
    <student_id>SV0001</student_id>
    <last_name>Nguyen</last_name>
    <first_name>Van A</first_name>
    <email>a.nguyen@example.com</email>
    <birth_date>2002-05-15</birth_date>
    <hometown>Ha Noi</hometown>
    <math_score>8.5</math_score>
    <literature_score>7.0</literature_score>
    <english_score>9.0</english_score>
  </student>
</students>
```

---

## 🔍 Crawler & Data Analysis

The crawler scrapes student data from the HTML table and performs statistical analysis using Pandas.

### Quick Run (No Python Required) 🐳

The easiest way to run the crawler is using Docker - **no Python installation needed!**

<details open>
<summary><b>Option 1: One-Click Script (Recommended)</b></summary>

```powershell
# Windows PowerShell
.\run_crawler.ps1

# Or Windows CMD
run_crawler.bat
```

This will:
1. ✅ Build the crawler Docker image
2. ✅ Run the crawler
3. ✅ Save output to `./output/students.xlsx`
4. ✅ Open the output folder

</details>

<details>
<summary><b>Option 2: Docker Command</b></summary>

```bash
# Build crawler image
docker build -t student-crawler ./crawler

# Run crawler (Windows PowerShell)
docker run --rm `
  -v "${PWD}/output:/app/output" `
  --network ppr501-final-project_default `
  student-crawler

# Run crawler (Linux/Mac)
docker run --rm \
  -v "$(pwd)/output:/app/output" \
  --network ppr501-final-project_default \
  student-crawler
```

</details>

<details>
<summary><b>Option 3: Local Python (if installed)</b></summary>

```bash
# Ensure Python 3.10+ is installed
python --version

# Install crawler dependencies
pip install -r crawler/requirements.txt

# Run crawler
python crawler/crawl_and_analyze.py
```

</details>

### Prerequisites

Before running the crawler, ensure Docker services are running:

```bash
# Check all containers are healthy
docker ps

# Expected output:
# ppr501-final-project-frontend-1   Up   0.0.0.0:3000->80/tcp
# ppr501-final-project-backend-1    Up   0.0.0.0:8000->8000/tcp
# ppr501-final-project-db-1         Up   0.0.0.0:5432->5432/tcp
```

### CLI Options (Local Python only)

```bash
# Default settings
python crawler/crawl_and_analyze.py

# Custom URL and output
python crawler/crawl_and_analyze.py \
  --url http://localhost:8000/students \
  --out output/students_analysis.xlsx
```

### Output Location

```bash
# The Excel file is created at:
# output/students.xlsx (default)
# or your specified --out path
```

### Output Excel Sheets

| Sheet Name | Description |
|------------|-------------|
| `raw` | Original crawled data without modifications |
| `cleaned` | Data after cleaning (normalized, parsed dates/scores) |
| `english_vs_math_corr` | Correlation matrix between English and Math scores |
| `english_vs_math_describe` | Descriptive statistics (mean, std, min, max, etc.) |
| `hometown_vs_english` | English score statistics grouped by hometown |
| `english_minus_math` | Score difference (English - Math) for each student |

### Analysis Details

#### 1. Correlation Analysis (english_vs_math_corr)
- **Purpose**: Measures the relationship between English and Math scores
- **Value Range**: -1 to 1
  - `1`: Perfect positive correlation
  - `0`: No correlation
  - `-1`: Perfect negative correlation

#### 2. Descriptive Statistics (english_vs_math_describe)
- **count**: Number of non-null values
- **mean**: Average score
- **std**: Standard deviation
- **min/max**: Score range
- **25%, 50%, 75%**: Quartile values

#### 3. Hometown Analysis (hometown_vs_english)
- Groups students by hometown
- Calculates English score statistics per hometown
- Sorted by count and mean score

#### 4. Score Comparison (english_minus_math)
- Shows difference: `English Score - Math Score`
- Positive: Better at English
- Negative: Better at Math

### Example Output

```
$ python crawler/crawl_and_analyze.py

Saved: D:\MSE\PPR501-Final-Project\output\students.xlsx
Correlation(english, math) = 0.0234
```

### Crawler CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | `http://localhost:8000/students` | URL of HTML page with students table |
| `--out` | `output/students.xlsx` | Output Excel file path |

---

## 💻 Development

### Code Quality Standards

| Standard | Description |
|----------|-------------|
| ✅ Type Hints | Full Python type annotations |
| ✅ Docstrings | All functions documented |
| ✅ JSDoc | JavaScript functions documented |
| ✅ Clean Architecture | Layered backend structure |
| ✅ Single Responsibility | Each module has one purpose |

### Design Patterns Used

- **Repository Pattern**: StudentService as data repository
- **Dependency Injection**: FastAPI Depends() for DB session
- **DTO Pattern**: Pydantic schemas for validation
- **Service Layer**: Business logic separation

### Running Locally (Development)

```bash
# Backend with hot-reload
cd backend
uvicorn app.main:app --reload

# Frontend with hot-reload
cd frontend
npm run dev
```

---

## 🔧 Troubleshooting

### Common Issues

<details>
<summary><b>🔴 Docker containers won't start</b></summary>

```bash
# Check Docker is running
docker info

# Remove old containers and volumes
docker compose down -v
docker compose up --build
```
</details>

<details>
<summary><b>🔴 Database connection error</b></summary>

```bash
# Wait for database to be healthy
docker compose logs db

# Recreate database
docker compose down -v
docker compose up --build
```
</details>

<details>
<summary><b>🔴 Frontend shows empty page</b></summary>

```bash
# Check backend is responding
curl http://localhost:8000/api/students

# Check frontend logs
docker compose logs frontend
```
</details>

<details>
<summary><b>🔴 Crawler fails with connection error</b></summary>

```bash
# Ensure backend is running
curl http://localhost:8000/students

# If HTML table not found, check the URL
python crawler/crawl_and_analyze.py --url http://localhost:8000/students
```
</details>

<details>
<summary><b>🔴 Crawler ImportError / pip not recognized</b></summary>

**Solution**: Use Docker instead of local Python!

```powershell
# Windows - Run the crawler via Docker
.\run_crawler.ps1

# Or use the batch file
run_crawler.bat
```

If you prefer local Python, install it from [python.org](https://www.python.org/).

```bash
# After installing Python
pip install -r crawler/requirements.txt
python crawler/crawl_and_analyze.py
```
</details>

### Reset Everything

```bash
# Complete reset (removes all data)
docker compose down -v
docker system prune -f
docker compose up --build
```

---

## 📄 License

This project is created for educational purposes as part of **PPR501 Final Project**.

---

<p align="center">
  Made with ❤️ by PPR501 Team
</p>
