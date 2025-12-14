# HBnB (AirBnB Clone) - The Console & Database

Welcome to the HBnB project! This repository contains a full-stack application that replicates the core functionality of AirBnB. It includes a command interpreter to manage your objects and a robust database engine for storage.

## 📂 Project Structure

This project is built to manage the following entities:
* **User:** Handles user registration and authentication.
* **Place:** Properties listed by users.
* **Review:** Feedback left by users for specific places.
* **Amenity:** Features available in a place (Wifi, AC, etc.).
* **PlaceAmenity:** Link table handling the Many-to-Many relationship between Places and Amenities.

## 🏗️ Database Architecture

The following Entity Relationship Diagram (ERD) illustrates the schema and relationships between the data models:

![Database Schema](part3/images/mermaid-diagram-2025-12-14-082756.png)

### Models Breakdown
* **User:** The root of the relationship, owning places and writing reviews.
* **Place:** The core entity, linked to a specific `User` (owner) and containing multiple `Reviews`.
* **Review:** Connects a `User` to a `Place` with a rating and text.
* **Amenity:** Features that can be shared across multiple places.

## 🚀 Getting Started

### Prerequisites
* Python 3.x
* MySQL (or your specific database)
* [Any other libraries, e.g., SQLAlchemy]

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up the environment:**
    ```bash
    # Example for setting up environment variables
    export HBNB_ENV=dev
    export HBNB_MYSQL_DB=hbnb_dev_db
    ```

4.  **Run the application:**
    ```bash
    python3 console.py
    ```

## 💻 Usage

Once the console is running, you can perform CRUD operations on the objects.

**Example:**
```bash
(hbnb) create User email="test@mail.com" password="123"
(hbnb) show User <user_id>
(hbnb) all Place
