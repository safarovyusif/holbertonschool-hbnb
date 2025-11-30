# Sequence Diagrams - HBnB Evolution

## Introduction
This document contains the Sequence Diagrams for the HBnB Evolution application. These diagrams detail the interaction flow between the User, the Presentation Layer (API), the Business Logic Layer (Facade & Models), and the Persistence Layer (Database) for four key use cases.

### 1. User Registration
**Description:** This sequence illustrates the process of registering a new user. The API receives the registration details, the Facade handles validation and business rules (e.g., checking if the email is unique), and finally, the User model is saved to the database.

```mermaid
sequenceDiagram
    actor User
    participant API as Presentation Layer (API)
    participant Facade as Business Logic (Facade)
    participant UserModel as User Model
    participant DB as Persistence Layer (Database)

    User->>API: POST /auth/register (details)
    API->>Facade: register_user(details)
    Facade->>UserModel: validate_email_uniqueness(email)
    
    alt Email already exists
        UserModel-->>Facade: Error: Email taken
        Facade-->>API: Error: Email taken
        API-->>User: 400 Bad Request
    else Email is unique
        Facade->>UserModel: create_user(details)
        UserModel->>DB: save()
        DB-->>UserModel: Success
        UserModel-->>Facade: User Object
        Facade-->>API: User Data (ID, Email)
        API-->>User: 201 Created
    end
