---
name: architecture-diagrams
description: Default skill for creating architecture diagrams. Use when user asks to draw architecture diagrams, system architecture, software architecture, infrastructure diagrams, component diagrams, deployment diagrams, or any visual representation of system structure. Always use Mermaid for diagrams.
---

# Architecture Diagrams

Default skill for creating all types of architecture diagrams using **Mermaid**.

## Default: Mermaid

Use Mermaid for all architecture diagrams. It renders natively on GitHub and supports various diagram types.

### Basic Example

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Web["Web App"]
        Mobile["Mobile App"]
    end
    
    subgraph API["API Layer"]
        Gateway["API Gateway"]
    end
    
    subgraph Service["Service Layer"]
        Auth["Auth Service"]
        User["User Service"]
    end
    
    Web --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> User
```

## Supported Diagram Types

### 1. Flowchart (流程图)
For processes, workflows, system architecture.

```mermaid
flowchart LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
    C --> D
```

### 2. Sequence Diagram (时序图)
For API interactions, message flows.

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB
    
    User->>API: POST /login
    API->>DB: Query credentials
    DB-->>API: Return user data
    API-->>User: Auth token
```

### 3. Class Diagram (类图)
For OOP design, entity relationships.

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +login()
    }
    
    class Order {
        +int id
        +float total
    }
    
    User "1" -- "*" Order : places
```

### 4. State Diagram (状态图)
For state machines, lifecycles.

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Success: complete
    Processing --> Error: fail
    Success --> [*]
    Error --> Idle: retry
```

### 5. ER Diagram (实体关系图)
For database schemas.

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : includes
```

## Architecture Diagram Types

### C4 Model

#### Level 1: System Context
```mermaid
flowchart TB
    User["👤 User<br/>[Person]"]
    System["🖥️ My System<br/>[Software System]"]
    External["🔗 External API<br/>[Software System]"]
    
    User -->|Uses| System
    System -->|Calls| External
```

#### Level 2: Container
```mermaid
flowchart TB
    subgraph Browser["Browser"]
        SPA["SPA<br/>[React]"]
    end
    
    subgraph "AWS" {
        APIGW["API Gateway<br/>[Nginx]"]
        
        subgraph "ECS" {
            Auth["Auth Service<br/>[Node.js]"]
            User["User Service<br/>[Node.js]"]
        }
        
        RDS[(PostgreSQL)]
    }
    
    SPA --> APIGW
    APIGW --> Auth & User
    Auth & User --> RDS
```

## Best Practices

1. **Use clear labels** - Every node should have a name
2. **Add technology tags** - [React], [PostgreSQL], [AWS Lambda]
3. **Show data flow** - Use directional arrows
4. **Group logically** - Use subgraphs for organization
5. **Keep it simple** - Split complex diagrams into multiple views

## Styling

### Default Style (Subgraphs with colors)
```mermaid
flowchart TB
    subgraph Frontend["Frontend Layer"]
        A["Web App"]
    end
    
    subgraph Backend["Backend Layer"]
        B["API Service"]
        C["Auth Service"]
    end
    
    A --> B --> C
```

### Minimal Style (Clean, ASCII-like layout)
For cleaner look, use simple boxes without heavy styling:

```mermaid
flowchart TB
    User["[User]"] --> API["[API Gateway]"]
    API --> Auth["[Auth Service]"]
    API --> UserSvc["[User Service]"]
    Auth --> DB["[(Database)]"]
    UserSvc --> DB
```

## References

- **Mermaid Syntax**: See `../mermaid-diagrams/SKILL.md`
- **Beautiful Mermaid**: See `../beautiful-mermaid/SKILL.md` - For themed SVG/PNG exports

## Decision Rule

```
Need architecture diagram?
    │
    └── Use Mermaid (always)
        │
        ├── GitHub/Web display → Mermaid code block
        │
        ├── Need themed export → Beautiful Mermaid
        │
        └── Simple diagram → Mermaid minimal style
```

**Always use Mermaid for architecture diagrams.**
