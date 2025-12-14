erDiagram
    User {
        string id PK "UUID"
        string first_name
        string last_name
        string email "Unique"
        string password
        boolean is_admin
    }

    Place {
        string id PK "UUID"
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK "References User"
    }

    Review {
        string id PK "UUID"
        string text
        int rating "1-5"
        string user_id FK "References User"
        string place_id FK "References Place"
    }

    Amenity {
        string id PK "UUID"
        string name "Unique"
    }

    Place_Amenity {
        string place_id PK,FK "References Place"
        string amenity_id PK,FK "References Amenity"
    }

    %% Relationships
    User ||--o{ Place : "owns (One-to-Many)"
    User ||--o{ Review : "writes (One-to-Many)"
    Place ||--o{ Review : "receives (One-to-Many)"
    Place ||--o{ Place_Amenity : "has"
    Amenity ||--o{ Place_Amenity : "included_in"
