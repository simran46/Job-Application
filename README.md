# Job-Application

# CareerPulse — Job Dashboard

A full-stack **Job Posting & Analytics Dashboard** built with:
- **Frontend**: Vue.js 3 + Vite (glassmorphic dark UI, custom SVG charts)
- **Backend**: Django 6 + Django REST Framework
- **Database**: PostgreSQL (auto-falls back to SQLite if Postgres is not running)

---

## 📁 Project Structure

```
interview_task/
├── backend/          ← Django REST API
│   ├── jobs/         ← Main app (models, views, serializers, tests)
│   ├── job_portal/   ← Project settings & URL config
│   ├── requirements.txt
│   └── manage.py
└── frontend/         ← Vue.js 3 + Vite app
    ├── src/
    │   ├── App.vue                    ← Main dashboard
    │   ├── components/
    │   │   ├── JobCard.vue            ← Job card with Edit/Delete/Duplicate
    │   │   ├── MultiSelect.vue        ← Custom multiselect dropdown
    │   │   ├── AnalyticsDashboard.vue ← Analytics modal (3 charts)
    │   │   └── DonutChart.vue         ← Custom SVG donut chart
    │   └── style.css                  ← Global design system
    └── package.json
```

---

## ⚙️ Prerequisites

Make sure you have the following installed:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.10+ | https://python.org |
| Node.js | 18+ | https://nodejs.org |
| PostgreSQL *(optional)* | 14+ | https://postgresql.org |

---

## 🚀 Setup & Run

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd interview_task
```

---

### 2. Backend Setup (Django)

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
```

✅ Backend API will be live at: **http://localhost:8000**

---

### 3. Frontend Setup (Vue.js)

Open a **new terminal window**:

```bash
# Go to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```

✅ Frontend app will be live at: **http://localhost:5173**

---

### 4. Open in Browser

Go to **http://localhost:5173** — the Vue app automatically connects to Django at port 8000.

---

## 🗄️ Database Configuration

This project uses **PostgreSQL** as its database. Configuration is managed using environment variables via a `.env` file inside the `backend` directory.

### Setup Instructions:

1. **Create the PostgreSQL Database:**
   Connect to your local PostgreSQL server and create a database named `myproject` (or any name of your choice):
   ```sql
   CREATE DATABASE myproject;
   ```

2. **Configure Environment Variables:**
   Navigate to the `backend/` directory, copy the `.env.example` file to a new file named `.env`, and update the database credentials to match your PostgreSQL setup:
   ```bash
   # Copy the example env file
   cp .env.example .env
   ```
   
   Open the `.env` file and set the variables:
   ```env
   SECRET_KEY=django-insecure-+$b*!#3o-u8mxctm!dq5%f=sl&1foltat@zjlhf^(!7b(h*y^s
   DEBUG=True

   DB_NAME=myproject
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. **Run Migrations:**
   Apply migrations to generate database tables:
   ```bash
   python manage.py migrate
   ```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Post a Job** | Full form with 10 fields including drag & drop image upload |
| **Multiselect Fields** | Custom dropdown for Status & Job Category with search |
| **Job Cards** | Rich UI cards showing all job info with color-coded status badges |
| **Edit Job** | Pre-filled modal form for editing existing postings |
| **Delete Job** | Smooth fade-out animation before removal |
| **Duplicate Job** | Creates an identical copy directly below the original card |
| **Analytics Dashboard** | Interactive SVG donut charts for Status, City & State distributions |

---
## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/jobs/` | List all jobs |
| `POST` | `/api/jobs/` | Create a new job |
| `PATCH` | `/api/jobs/<id>/` | Edit a job |
| `DELETE` | `/api/jobs/<id>/` | Delete a job |
| `POST` | `/api/jobs/<id>/duplicate/` | Duplicate a job |
