<p align="center">
  <h1 align="center">🎓 Student Management System</h1>
  <p align="center">
    <strong>Desktop + API application for managing student records</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
    <img src="https://img.shields.io/badge/Tkinter-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter"/>
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
- **Desktop UI** with Tkinter (Windows-friendly)
- **Built-in Charts** with Seaborn/Matplotlib
- **Data Analysis** capabilities with Pandas
- **Containerized** deployment with Docker Compose

### Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| **Backend** | FastAPI, SQLAlchemy, Pydantic | Python 3.11 |
| **Desktop App (UI)** | Tkinter + requests + Matplotlib/Seaborn | Python 3.10+ |
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
| ✅ **Desktop UI** | Tkinter với giao diện trực quan |
| ✅ **Charts** | Biểu đồ thống kê với Seaborn/Matplotlib |
| ✅ **Data Crawler** | Phân tích dữ liệu từ XML API |
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

# 3. Start backend services (db + api)
docker compose up --build -d db backend
```

🎉 **Done!** Access the services:

| Service | URL |
|---------|-----|
| 🖥 Desktop App | Run locally (Tkinter) |
| 📖 API Docs | http://localhost:8000/docs |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Download |
|-------------|---------|----------|
| Docker Desktop | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

> 📝 **Note**: Python is NOT required! The crawler runs via Docker.

> 📝 **Desktop app note**: The Tkinter desktop app runs locally, so it requires Python 3.10+ on your machine.

---

## 🔧 Installation

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd PPR501-Final-Project

# Create environment configuration
cp .env.example .env

# Build and start backend services
docker compose up --build -d db backend

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

</details>

---

## 📖 Usage

### Desktop App (Tkinter)

The desktop app is the primary UI.

#### Option A (Recommended): Backend via Docker + Desktop UI local

1) Start backend:

```bash
docker compose up --build -d db backend
```

2) Install Python 3.10+ (Windows):
- Download: https://www.python.org/downloads/
- During install, check **"Add Python to PATH"**

3) Create virtual environment + install deps:

```powershell
cd desktop_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Alternatively (one-click from project root):

```powershell
.\run_desktop.ps1
```

4) Run the desktop app:

```powershell
cd ..
python -m desktop_app.app --api http://localhost:8000/api
```

Trong app, tab **Thống kê** hiển thị biểu đồ phân tích điểm số và phân bố theo quê quán.

#### Option B: Run backend locally (no Docker)

If you want to run everything without Docker, you can run FastAPI locally.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Set DATABASE_URL (example; adjust credentials/host if needed)
$env:DATABASE_URL = "postgresql+psycopg2://students_user:students_pass@localhost:5432/students_db"

uvicorn app.main:app --reload --port 8000
```

Note: local backend still requires a PostgreSQL database (you can keep only db in Docker: `docker compose up -d db`).

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
├── 📂 desktop_app/             # Tkinter Desktop App (Primary UI)
│   ├── app.py
│   ├── charts.py
│   ├── student_api.py
│   ├── xml_parser.py
│   └── requirements.txt
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

### 📌 Giải thích cấu trúc & ý nghĩa từng file/folder

#### backend/
- app/main.py: Khởi tạo FastAPI app, CORS, router, health check.
- app/api/v1/endpoints/students.py: CRUD XML endpoints cho sinh viên.
- app/core/: cấu hình và kết nối database.
- app/models/: ORM models.
- app/schemas/: Pydantic schemas cho validate dữ liệu.
- app/services/: business logic (StudentService).
- app/utils/: xử lý XML + làm sạch dữ liệu.
- Dockerfile: build backend container.
- requirements.txt: dependencies backend.

#### desktop_app/
- app.py: UI chính (Tkinter), table + form CRUD + tab biểu đồ.
- charts.py: tạo biểu đồ thống kê bằng seaborn/matplotlib.
- student_api.py: client gọi API XML.
- xml_parser.py: parse XML -> StudentRecord + tạo payload JSON.
- requirements.txt: dependencies desktop app.

#### crawler/
- crawl_and_analyze.py: crawl từ XML API, phân tích, export Excel.
- Dockerfile: build crawler container.
- requirements.txt: dependencies crawler.

#### docker/
- db/init.sql: schema + seed dữ liệu.
- db/students.csv: 100 dữ liệu mẫu.

#### scripts
- run_desktop.ps1 / run_desktop.bat: chạy desktop app (one-click).
- run_crawler.ps1 / run_crawler.bat: chạy crawler (one-click).

---

## 🏗 Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Compose                            │
├─────────────────┬─────────────────────┬─────────────────────────┤
│                 │                     │                         │
│  ┌───────────┐  │  ┌───────────────┐  │  ┌─────────────────┐   │
│  │ Desktop   │  │  │    Backend    │  │  │   PostgreSQL    │   │
│  │ (Tkinter) │──┼──│   (FastAPI)   │──┼──│   (Database)    │   │
│  │  local    │  │  │    :8000      │  │  │     :5432       │   │
│  └───────────┘  │  └───────────────┘  │  └─────────────────┘   │
│        │        │         │           │           │             │
│   HTTP Client   │    REST API (XML)   │     100 Students       │
│   requests      │────────>│           │        Seeded          │
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

The crawler reads data from the **XML API** and performs statistical analysis using Pandas.

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
# ppr501-final-project-backend-1    Up   0.0.0.0:8000->8000/tcp
# ppr501-final-project-db-1         Up   0.0.0.0:5432->5432/tcp
```

### CLI Options (Local Python only)

```bash
# Default settings
python crawler/crawl_and_analyze.py

# Custom URL and output
python crawler/crawl_and_analyze.py \
  --url http://localhost:8000/api/students \
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
| `--url` | `http://localhost:8000/api/students` | XML API endpoint |
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
<summary><b>🔴 Crawler fails with connection error</b></summary>

```bash
# Ensure backend is running
curl http://localhost:8000/api/students

# If API not found, check the URL
python crawler/crawl_and_analyze.py --url http://localhost:8000/api/students
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
