# HBnB Evolution - Part 2 (Backend)

This repository contains the backend implementation of the HBnB project, built using Python, Flask, and Flask-RESTx. It follows a modular architecture with a Facade pattern to manage communication between the API and the In-Memory Repository.

## 📂 Project Structure
- **app/models/**: Core business logic (User, Place, Review, Amenity).
- **app/api/v1/**: API endpoints defined with Flask-RESTx.
- **app/services/**: Facade pattern implementation.
- **app/persistence/**: In-memory data storage (Repository).
- **tests/**: Unit tests for validating API endpoints.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
