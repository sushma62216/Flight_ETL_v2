# Flight Data ETL Pipeline with Orchestration and Containerisation

## About the Project

This project demonstrates a real-time ETL pipeline that ingests flight data from the OpenSky Network API, processes it using Python, orchestrates the workflow using Apache Airflow, stores the cleaned data in PostgreSQL, and visualizes it using Streamlit.

The entire pipeline is containerized using Docker Compose, ensuring isolated, repeatable, and portable execution across environments. DBeaver is used to inspect and query the database visually.

---

## Technologies & Skills Demonstrated

| Category              | Tool                         |
|-----------------------|--------------------------------------|
| 🐍 Programming        | **Python** – API requests, data parsing, DB interaction |
| 🔄 Workflow Orchestration | **Apache Airflow** – DAG creation, task scheduling, automation |
| 🐳 Containerization   | **Docker** & **Docker Compose** – Service orchestration |
| 🗄️ Database           | **PostgreSQL** – Relational data storage and schema design |
| 🖥️ Database Client    | **DBeaver** – GUI for browsing PostgreSQL tables and data |
| 📊 Data Visualization | **Streamlit** – Real-time dashboard for displaying flight data |
| 🌐 External API       | **OpenSky Network API** – Real-time flight data ingestion |

---


### ETL Workflow (Step-by-Step)

1. **DAG Triggered (Airflow)**  
   Airflow Scheduler activates the DAG based on its schedule or manual trigger.

2. **Extract (Python)**  
   `extract.py` sends a GET request to the OpenSky API (HTTPS over port 443) to fetch live flight data in JSON format.

3. **Transform**  
   `transform.py` parses, cleans, and structures the API response, extracting fields like `icao24`, `callsign`, `origin_country`, etc.

4. **Load (PostgreSQL)**  
   `load.py` connects to the PostgreSQL container (port 5432) and inserts the cleaned data into structured tables.

5. **Monitor (Airflow UI)**  
   DAG execution and task logs can be monitored via Airflow Web UI at [http://localhost:8080](http://localhost:8080).

6. **Streamlit Visualization**
   The project features a **Streamlit app** that reads from PostgreSQL and displays recent flight data in an interactive dashboard.

---

#### To Run Streamlit:

```bash
streamlit run streamlit_app.py
---
## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker & Docker Compose
- Python 3.8+
- Git

### Clone the Repository

```bash
git clone https://github.com/yourusername/Flight_ETL_v2.git
cd Flight_ETL_v2

