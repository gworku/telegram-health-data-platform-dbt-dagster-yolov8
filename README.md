# End-to-End Data Platform for Ethiopian Medical Telegram Dat

## Project Overview
This project involves creating a data warehouse for **Kara Solutions**, designed to store and analyze data on Ethiopian medical businesses scraped from **Telegram channels**. The goal is to derive insights into trends and patterns within the medical sector in Ethiopia. The project includes:

- **Data scraping** from Telegram
- **Data cleaning and transformation** using DBT
- **Object detection** with YOLO
- **API development** with FastAPI
- **Data warehouse implementation** in PostgreSQL

---
## Data Collection

Data was collected from **Telegram channels** using the `Telethon` library.

### **Steps:**
1. **Telethon API:** Connected to the Telegram API to extract text and metadata.
2. **Logging:** Implemented logging to track the scraping process.
3. **Storage:** Temporarily stored raw data before processing.

---
## Data Cleaning and Transformation

Using **DBT (Data Build Tool)**, data cleaning and transformations were performed to ensure high-quality, structured data.

### **Processes:**
- **Data Cleaning:** Removed duplicates, handled missing values, and standardized text fields.
- **Data Transformation:** Utilized **DBT models** to structure and transform data for consistency and analysis.

---
## Object Detection with YOLO

YOLO (`You Only Look Once`) was implemented for **object detection** in images, enabling the analysis of visual data related to Ethiopian medical businesses.

### **Steps:**
1. **Setup:** Configured **YOLOv5**, installing dependencies like `OpenCV` and `PyTorch`.
2. **Detection:** Processed images to detect objects and stored results in **PostgreSQL**.

---
## API Development with FastAPI

To make the data warehouse accessible, an API was developed using **FastAPI**.

### **Features:**
- **Endpoints** for querying medical business data
- **Authentication & security** best practices implemented
- **Optimized response times** with asynchronous processing

---
## Installation

### **1. Clone the repository:**
```bash
git clone https://github.com/gworku/telegram-health-data-platform-dbt-dagster-yolov8.git
cd telegram-health-data-platform-dbt-dagster-yolov8

### **2. Install dependencies:**
```bash
pip install -r requirements.txt
```

### **3. Set up PostgreSQL and DBT:**
- Configure your **PostgreSQL database**.
- Run `dbt run` to execute transformations.

### **4. Run YOLO and FastAPI:**
Follow the instructions in the `yolo` and `api` directories.

---
## Usage
To start the FastAPI server, run:
```bash
uvicorn app.main:app --reload
```
Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

