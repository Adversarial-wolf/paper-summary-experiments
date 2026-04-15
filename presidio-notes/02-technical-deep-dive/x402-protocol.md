# 🔗 x402 Protocol Mechanics

## Protocol Flow (Standard)
```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant Server as 402 Payment Server
    participant Facilitator as Facilitator API
    participant Chain as Base L2
    
    Agent->>Server: GET /resource
    Server-->>Agent: HTTP 402 + Payment-Required header
    Agent->>Agent: Construct EIP-712 typed data:
    Note right of Agent: {<br/>  resource_url: "...",<br/>  description: "...",<br/>  reason: "...",<br/>  amount: "0.50",<br/>  timestamp: 1713189022<br/>}
    Agent->>Agent: Sign with wallet private key
    Agent->>Server: Retry GET with X-Payment: <signed-token>
    Server->>Facilitator: POST /validate {token}
    Facilitator->>Chain: Execute USDC transfer
    Chain-->>Facilitator: Transaction receipt
    Facilitator-->>Server: {valid: true}
    Server-->>Agent: 200 OK + resource
```

## Metadata Fields at Risk
| Field | Typical Content | PII Risk Examples |
|-------|----------------|-------------------|
| `resource_url` | API endpoint path | `/patient/alice.martin%40corp.io/export` |
| `description` | Human-readable purpose | "Export records for Alice Martin" |
| `reason` | Business justification | "User alice@example.com requested GDPR export" |

## EIP-712 Typed Data Structure
```json
{
  "types": {
    "Payment": [
      {"name": "resource_url", "type": "string"},
      {"name": "description", "type": "string"},
      {"name": "reason", "type": "string"},
      {"name": "amount", "type": "uint256"},
      {"name": "timestamp", "type": "uint256"}
    ]
  },
  "primaryType": "Payment",
  "domain": {"name": "x402", "version": "1", "chainId": 8453},
  "message": { ... }
}
```

> ⚠️ **Critical**: The `message` object is signed *as-is*. If it contains PII, that PII is cryptographically bound to the payment token and transmitted to all downstream parties.

## Why Post-Hoc Redaction Doesn't Work
```mermaid
graph LR
    A[Agent Signs Token with PII] --> B[Token Transmitted to Server]
    B --> C[Server Forwards to Facilitator]
    C --> D[Facilitator Logs/Processes Metadata]
    D --> E[Post-Hoc Redaction Attempt]
    E --> F[❌ Too Late: PII Already Exposed]
    
    style F fill:#ffebee,stroke:#c62828
```

**Architectural Solution**: Intercept and filter *before* signing and transmission.
