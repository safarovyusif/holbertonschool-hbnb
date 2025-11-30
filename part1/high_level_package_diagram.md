# High-Level Package Diagram - HBnB Evolution

## Architecture Overview
The HBnB Evolution application follows a structured **three-layer architecture**. This design separates concerns, making the system maintainable and scalable. The communication between the Presentation Layer and the Business Logic Layer is strictly managed via the **Facade Pattern**.

### Package Diagram (Mermaid)

```mermaid
classDiagram
    classPresentationLayer {
        <<Interface>>
        +ServiceAPI
    }

    classBusinessLogicLayer {
        +HBnBFacade
        +User
        +Place
        +Review
        +Amenity
    }

    classPersistenceLayer {
        +DataRepository
    }

    %% Relationships
    classPresentationLayer --> classBusinessLogicLayer : Uses (Facade Interface)
    classBusinessLogicLayer --> classPersistenceLayer : Database Operations
