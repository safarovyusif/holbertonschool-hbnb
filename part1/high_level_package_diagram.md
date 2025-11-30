# High-Level Package Diagram - HBnB Evolution

## Architecture Overview
The HBnB Evolution application follows a structured **three-layer architecture**. This design separates concerns, making the system maintainable and scalable. The communication between the Presentation Layer and the Business Logic Layer is strictly managed via the **Facade Pattern**.

### Package Diagram (Mermaid)

```mermaid
classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
    }

    class BusinessLogicLayer {
        +HBnBFacade
        +User
        +Place
        +Review
        +Amenity
    }

    class PersistenceLayer {
        +DataRepository
    }

    %% Relationships
    PresentationLayer --> BusinessLogicLayer : Uses (Facade Interface)
    BusinessLogicLayer --> PersistenceLayer : Database Operations
