# Inclusive AI Map

A Streamlit-based web application for visualizing language model data with PostgreSQL and PostGIS integration.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: Running with Docker (Recommended)](#option-1-running-with-docker-recommended)
  - [Option 2: Running Locally](#option-2-running-locally)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Setup
- Docker
- Docker Compose

### For Local Setup
- Python 3.12.8
- PostgreSQL 16 with PostGIS extension
- pip (Python package manager)

## Installation

### Option 1: Running with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd inclusiveai_map
   ```

2. Create a `.env` file in the root directory:
   ```bash
   PGUSER=postgres
   PGPASSWORD=password123
   PGHOST=db
   PGPORT=5432
   PGDATABASE=inclusiveai_map
   DATABASE_URL=postgresql://postgres:password123@db:5432/inclusiveai_map
   ```

3. Build and start the containers:
   ```bash
   docker compose up --build
   ```

4. The application will be available at http://localhost:8000

### Option 2: Running Locally

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd inclusiveai_map
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

### For Docker Setup
The database will be automatically created and configured when you run `docker compose up`.

### For Local Setup

1. Make sure PostgreSQL is running:
   ```bash
   pg_isready
   ```

2. Create the database and enable PostGIS:
   ```bash
   createdb inclusiveai_map
   psql -d inclusiveai_map -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS postgis_topology;"
   ```

3. Restore the database from backup:
   ```bash
   psql -d inclusiveai_map -f data/xri_backup123124.sql
   ```

## Environment Variables

### For Local Setup
Set the following environment variables:
```bash
export PGUSER=your_username
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=inclusiveai_map
export DATABASE_URL=postgresql://your_username@localhost:5432/inclusiveai_map
```

Replace `your_username` with your PostgreSQL username.

## Running the Application

### With Docker
```bash
docker compose up
```

### Locally
```bash
streamlit run main.py --server.port 8000
```

The application will be available at http://localhost:8000

## Troubleshooting

### Common Issues

1. **Port 5000/8000 already in use**
   ```bash
   # Check what's using the port
   lsof -i :5000  # or :8000
   # Use a different port
   streamlit run main.py --server.port 8501
   ```

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check environment variables are set correctly
   - Ensure PostGIS extension is installed

3. **Docker Issues**
   ```bash
   # Stop all containers and remove volumes
   docker compose down -v
   # Rebuild from scratch
   docker compose up --build
   ```

### PostgreSQL Commands

Check database status:
```bash
psql -d inclusiveai_map -c "\dt"  # List tables
psql -d inclusiveai_map -c "\dx"  # List extensions
```

For any additional issues or questions, please open an issue in the repository.
