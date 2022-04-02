### API  to connect and retrieve data from Youtube
```mermaid
graph   LR
    subgraph Retriever
    A{Connector to Video URL} -->|Get connection as BS4/HTML object| B{Youtube Video Data Retriever}
    
    B --> D[Get Title]
    B --> F[Get Views Count]
    B --> E[Get Likes/Dislikes]
    B --> G[Get Upload Date]
    D --> I[(Logger)]
    F --> I[(Logger)]
    E --> I[(Logger)]
    G --> I[(Logger)]
    end
    subgraph Analyzer
    J[Current Date] --> I[(Logger)]
    I[(Logger)] --> |Connector| K{Youtube Analyzer}
    end
```