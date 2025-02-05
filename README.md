# Inclusive AI Map

A Streamlit-based web application for visualizing language model data with PostgreSQL and PostGIS integration.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Environment Setup](#environment-setup)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Python 3.12.8
- PostgreSQL 16 with PostGIS extension
- pip (Python package manager)

## Installation

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

## Database Setup

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

## Environment Setup

Before running the application, you need to set up the environment variables in your terminal. Run the following commands:

```bash
export PGUSER=suvrkamaldas
export PGPASSWORD=password123
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=inclusiveai_map
export DATABASE_URL=postgresql://suvrkamaldas:password123@localhost:5432/inclusiveai_map
```

**Note**: These environment variables must be set in your terminal before starting the application. They need to be set every time you open a new terminal session.
export PGPORT=5432
export PGDATABASE=inclusiveai_map
export DATABASE_URL=postgresql://your_username@localhost:5432/inclusiveai_map
```

Replace `your_username` with your PostgreSQL username.

## Running the Application

```bash
streamlit run main.py --server.port 8000
```

The application will be available at http://localhost:8501

```

(venv) suvrkamaldas@Subhros-MacBook-Air inclusiveai_map % export PGUSER=suvrkamaldas PGPASSWORD=password123 PGHOST=localhost PGPORT=5432 PGDATABASE=inclusiveai_map DATABASE_URL=postgresql://suvrkamaldas:password123@localhost:5432/inclusiveai_map
(venv) suvrkamaldas@Subhros-MacBook-Air inclusiveai_map % streamlit run main.py --server.port 8501

```


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


### PostgreSQL Commands

Check database status:
```bash
psql -d inclusiveai_map -c "\dt"  # List tables
psql -d inclusiveai_map -c "\dx"  # List extensions
```

For any additional issues or questions, please open an issue in the repository.
