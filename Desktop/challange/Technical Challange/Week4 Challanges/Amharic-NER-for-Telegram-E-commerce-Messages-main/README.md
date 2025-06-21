# Amharic-NER-for-Telegram-E-commerce-Messages 
# 
## Project Overview  
Amharic-NER-for-Telegram-E-commerce-Messages centralizes e-commerce activities from various Ethiopian-based Telegram channels, enabling real-time data extraction to create a unified platform. This project focuses on:  

- Extracting real-time data (text, images, documents) from Telegram channels such as `@ZemenExpress`.  
- Fine-tuning a large language model (LLM) for Amharic Named Entity Recognition (NER).  
- Identifying key entities such as products, prices, and locations in Amharic text.  

This repository contains code for data ingestion, preprocessing, and labeling for NER tasks, supporting EthioMart’s vision of a seamless e-commerce platform.  

## Features  

### Real-Time Data Ingestion  
- A custom scraper connects to Telegram channels and fetches messages, images, and metadata.  

### Text Preprocessing  
- Includes tokenization, normalization, and handling Amharic-specific linguistic features.  

### NER Labeling  
- Annotates text data for NER tasks in the CoNLL format, labeling:  
  - **Products**: `B-Product`, `I-Product`  
  - **Prices**: `B-PRICE`, `I-PRICE`  
  - **Locations**: `B-LOC`, `I-LOC`  

## Requirements  
Install the required libraries using the following command:  

```bash  
pip install -r requirements.txt  
