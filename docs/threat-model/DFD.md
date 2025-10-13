# DFD — Data Flow Diagram

## Diagram (Mermaid)
```mermaid
flowchart LR
  U[User/Client] -->|F1: HTTPS| API[FastAPI app]
  subgraph Edge[Trust Boundary: Edge]
    API --> SVC[Decks/Cards Service]
  end
  subgraph Core[Trust Boundary: Core]
    SVC --> MEM[(In-Memory Storage)]
  end

  %% optional integrations
  U -->|F2: HTTPS| Docs[OpenAPI/Swagger UI]
```

## Flows
| ID | Source → Target | Channel/Protocol | Data/PII | Notes |
|----|------------------|------------------|----------|-------|
| F1 | U → API         | HTTPS            | generic  | Requests to `/decks`, `/cards`, `/health` |
| F2 | U → Docs        | HTTPS            | none     | Read-only OpenAPI UI |
| F3 | API → SVC       | in-proc call     | payloads | Pydantic validation, error envelope |
| F4 | SVC → MEM       | memory           | cards PI | In-memory lists emulate storage |
