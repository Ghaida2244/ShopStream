# ShopStream

Ghaida Alomar

ShopStream is a data engineering project that processes online retail transaction data.

The project will receive transaction records, validate the data, separate invalid records, store the valid data in Bronze, Silver, and Gold layers, and apply data quality checks.

It will also include a RAG system that searches documents and gives answers based on the retrieved information.

## Dataset

The project uses the Online Retail dataset. It includes invoice numbers, product details, quantity, price, customer ID, invoice date, and country.

## Tools

- Apache Kafka
- Pydantic
- Delta Lake
- Apache Airflow
- Great Expectations
- OpenLineage
- Vector Database
- RAG

## Training Program

Modern Data Engineering for AI Systems  
SDAIA Academy  
June 2026

## Current Progress

Project setup completed.

## Project Overview

ShopStream is a retail data engineering pipeline.

The system:

- Receives retail data using Apache Kafka
- Validates records using Pydantic
- Stores invalid records in quarantine
- Stores valid records in the Bronze layer
- Cleans and transforms data in the Silver layer
- Checks data quality using Great Expectations
- Creates summary data in the Gold layer
- Uses Apache Airflow to run the pipeline
- Uses ChromaDB for semantic search

## Technologies

- Python
- Kafka
- Airflow
- Docker
- Delta Lake
- Great Expectations
- OpenLineage
- ChromaDB

## Pipeline

```text
Kafka
  ↓
Validation
  ↓
Bronze
  ↓
Silver
  ↓
Quality Check
  ↓
Gold