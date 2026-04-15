# 📚 Glossary: Key Terms & Acronyms

## Protocol & Infrastructure
| Term | Definition |
|------|------------|
| **x402** | HTTP-native micropayment protocol extending HTTP 402 Payment Required; uses EIP-712 signed tokens and stablecoin settlement on Base L2 |
| **Facilitator API** | Centralized service that validates x402 payment tokens and executes on-chain USDC transfers; acts as settlement oracle |
| **EIP-712** | Ethereum standard for typed structured data hashing and signing; enables human-readable payment token verification |
| **Base L2** | Coinbase's Ethereum Layer 2 network; low-cost, high-throughput chain for x402 settlement |
| **USDC** | USD Coin, a fiat-collateralized stablecoin used for x402 settlements |

## Security & Privacy
| Term | Definition |
|------|------------|
| **PII (Personally Identifiable Information)** | Data that can identify an individual: names, emails, SSNs, IBANs, phone numbers, etc. |
| **Pre-execution filtering** | Security control applied *before* data leaves the trust boundary; contrasts with post-hoc monitoring |
| **Fail-safe vs. fail-open** | Fail-safe: errors block operations (safe but potentially disruptive); fail-open: errors allow operations (convenient but risky). This middleware uses fail-safe. |
| **Zero-trust metadata** | Design principle: treat all incoming metadata as potentially adversarial; never trust content based on source reputation alone |
| **Data minimisation** | GDPR principle: collect and process only the personal data strictly necessary for the specified purpose |

## Compliance & Governance
| Term | Definition |
|------|------------|
| **GDPR Art. 5(1)(c)** | Data minimisation principle: personal data shall be "adequate, relevant and limited to what is necessary" |
| **GDPR Art. 28** | Processor obligations: controllers must bind data processors via contract with specific data protection clauses |
| **DPIA (Data Protection Impact Assessment)** | Mandatory risk assessment for high-risk processing under GDPR; this middleware reduces DPIA scope by design |
| **DSAR (Data Subject Access Request)** | Individual's right to access/delete their personal data; audit logs enable efficient response |
| **DPA (Data Processing Agreement)** | Contractual instrument required under GDPR Art. 28 when engaging processors |

## Technical Components
| Term | Definition |
|------|------------|
| **Presidio** | Microsoft's open-source SDK for PII detection and anonymisation; uses regex patterns + spaCy NLP for entity recognition |
| **spaCy** | Industrial-strength NLP library; provides named entity recognition (NER) for PERSON detection |
| **Micro-F1** | Harmonic mean of precision and recall, averaged across all entity types; primary metric for PII filter effectiveness |
| **p99 latency** | 99th percentile response time; metric for worst-case performance (more meaningful than average for SLAs) |
| **HMAC-SHA256 fingerprint** | Cryptographic hash of payment token fields + timestamp; used for replay detection with TTL-bounded deduplication |
| **JSON-L** | JSON Lines format: one JSON object per line; efficient for streaming audit logs |

## Metrics & Evaluation
| Term | Definition |
|------|------------|
| **Precision** | % of redacted entities that were truly PII (low false positives) = TP / (TP + FP) |
| **Recall** | % of true PII entities that were successfully redacted (low false negatives) = TP / (TP + FN) |
| **F1 Score** | Harmonic mean of precision and recall; balances both concerns = 2 × (P × R) / (P + R) |
| **Synthetic corpus** | Artificially generated dataset with known ground truth; enables reproducible evaluation without live PII |
| **Parameter sweep** | Systematic evaluation across multiple configuration dimensions to identify optimal settings |

## Project-Specific
| Term | Definition |
|------|------------|
| **presidio-hardened-x402** | The open-source middleware presented in this paper; not to be confused with Microsoft Presidio SDK |
| **HardenedX402Client** | Python class implementing the 4-control pipeline; drop-in replacement for Coinbase's x402 client |
| **PIIFilter / PolicyEngine / ReplayGuard / AuditLog** | The four sequential security controls applied to every outbound payment request |
| **min_score** | Confidence threshold for PII detection; higher values increase precision but reduce recall |

## Acronyms
| Acronym | Expansion |
|---------|-----------|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| DPA | Data Processing Agreement |
| DPIA | Data Protection Impact Assessment |
| DSAR | Data Subject Access Request |
| EIP | Ethereum Improvement Proposal |
| F1 | Harmonic mean of Precision and Recall |
| GDPR | General Data Protection Regulation (EU) |
| HMAC | Hash-based Message Authentication Code |
| IBAN | International Bank Account Number |
| L2 | Layer 2 (blockchain scaling solution) |
| NER | Named Entity Recognition |
| NLP | Natural Language Processing |
| PII | Personally Identifiable Information |
| P/R/F1 | Precision / Recall / F1 Score |
| RTT | Round-Trip Time (network) |
| SIEM | Security Information and Event Management |
| SSN | Social Security Number (US) |
| TTL | Time-To-Live (cache/store expiration) |
| USDC | USD Coin (stablecoin) |
| WORM | Write-Once-Read-Many (audit storage) |
