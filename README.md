### API  to connect and retrieve data from Youtube
```mermaid
graph   LR
    subgraph Connector/Transformer
    A{Connector to Video URL} -->|Get connection as BS4/HTML object| B{Youtube Video Data Retriever}
    
    B --> D[Title]
    B --> F[Views Count]
    B --> E[Likes/Dislikes]
    B --> G[Upload Date]
    B --> H[Duration]
    end
    subgraph Logger
    D --> I[(Logger)]
    F --> I[(Logger)]
    E --> I[(Logger)]
    G --> I[(Logger)]  
    H --> I[(Logger)]  
    end
    subgraph Analyzer
    J[Current Date] -.-> I[(Logger)]
    I[(Logging Module/DB)] --> |Listener| K{Youtube Analyzer}
    end
```