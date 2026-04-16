# ⚠️ Limitations & Future Work

## Current Limitations

### Technical Limitations
| Limitation | Impact | Workaround |
|------------|--------|------------|
| **PERSON recall = 0.551 in URL paths** | ~45% of name-bearing tokens may not be redacted | Slug-aware preprocessing; manual review for high-risk categories |
| **English-only NLP model** | Non-Latin script PII not detected | Deploy language-specific Presidio models; restrict to English domains initially |
| **No adversarial obfuscation handling** | Base64/homoglyph attacks may bypass filter | Monitor for suspicious patterns; plan v0.3.0 enhancements |
| **Synthetic corpus prevalence estimates** | Real-world PII rates may differ | Plan live-data validation study; monitor production detection rates |

### Operational Limitations
| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Fail-safe blocking may disrupt workflows** | Legitimate payments blocked on false positives | Implement retry logic with human review for blocked requests |
| **Redis dependency for scale** | Single-node deployments use less robust in-memory store | Document fallback behavior; recommend Redis for production |
| **Audit log storage requirements** | High-volume deployments generate significant log data | Implement log rotation; forward to scalable SIEM platform |

### Compliance Limitations
| Limitation | Impact | Guidance |
|------------|--------|----------|
| **Residual false negative risk** | Cannot guarantee 100% PII detection | Document in DPIA; implement compensating controls (manual review) |
| **Facilitator legal characterisation** | Jurisdiction-dependent interpretation of "processor" status | Consult legal counsel; use redaction to simplify DPA requirements |
| **Cross-border data flow implications** | Redacted metadata may still enable re-identification | Conduct transfer impact assessments; apply additional anonymisation if needed |

## Future Work Roadmap

### v0.2.1 (Q3 2026)
- [ ] Live-data validation study on Base L2 traffic
- [ ] Multilingual NLP support (spaCy models for DE, FR, ES)
- [ ] Enhanced slug-aware preprocessing for PERSON detection
- [ ] Prometheus/Grafana metrics exporter

### v0.3.0 (Q4 2026)
- [ ] Adversarial obfuscation detector module
- [ ] Multi-party authorisation for high-value payments
- [ ] Policy engine: dynamic limits based on risk scoring
- [ ] Audit log: blockchain-anchored integrity proofs

### Research Directions
- [ ] Federated learning for domain-adapted PII detection
- [ ] Zero-knowledge proofs for policy compliance verification
- [ ] Protocol-level extensions: encrypted metadata fields
- [ ] Cross-agent policy coordination for swarm deployments

## Contribution Guidelines
```markdown
We welcome contributions to address limitations and implement future work:

1. **Bug reports**: Include minimal reproducible example + environment details
2. **Feature requests**: Describe use case + proposed solution + risk assessment
3. **Code contributions**: Follow PEP 8, include tests, update documentation
4. **Domain recognizers**: Submit new entity patterns with validation corpus

Repository: https://github.com/presidio-v/presidio-hardened-x402
License: MIT (permissive for commercial and research use)
```

> 💡 **Key Message**: *"This is a living project. The limitations documented here are not dead ends—they are invitations to collaborate on building more privacy-preserving AI infrastructure."*
