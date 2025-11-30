# Detailed Class Diagram - Business Logic Layer

## Introduction
This document illustrates the Detailed Class Diagram for the Business Logic Layer of the HBnB Evolution application. It defines the core entities, their attributes, methods, and relationships. All entities inherit from a common `BaseModel` to ensure consistency in ID generation and audit timestamps.

### Class Diagram (Mermaid)

```mermaid
classDiagram
    %% Parent Class for common attributes
    class BaseModel {
        +UUID4 id
        +DateTime created_at
        +DateTime updated_at
        +save()
        +update()
    }

    %% User Entity
    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register()
        +update_profile()
        +delete()
    }

    %% Place Entity
    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +UUID4 owner_id
        +create()
        +update()
        +delete()
        +list()
    }

    %% Review Entity
    class Review {
        +Float rating
        +String comment
        +UUID4 user_id
        +UUID4 place_id
        +create()
        +update()
        +delete()
        +list_by_place()
    }

    %% Amenity Entity
    class Amenity {
        +String name
        +String description
        +create()
        +update()
        +delete()
        +list()
    }

    %% Relationships

    %% 1. Inheritance (All classes inherit from BaseModel)
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% 2. User - Place Relationship (One User owns Many Places)
    User "1" *-- "0..*" Place : Owns

    %% 3. User - Review Relationship (One User writes Many Reviews)
    User "1" *-- "0..*" Review : Writes

    %% 4. Place - Review Relationship (One Place has Many Reviews)
    Place "1" *-- "0..*" Review : Has

    %% 5. Place - Amenity Relationship (Many-to-Many)
    Place "0..*" o-- "0..*" Amenity : Has
