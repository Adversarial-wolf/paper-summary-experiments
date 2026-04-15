# ⚙️ Configuration Recipes: Production Deployment Patterns

## 🎯 Recommended Baseline (Start Here)
```yaml
# config/recommended.yaml
pii_filter:
  mode: nlp                    # Use spaCy NER for PERSON detection
  min_score: 0.4              # Balance precision/recall per paper findings
  entities:                   # All 6 entity types—PHONE adds 2pp recall at negligible cost
    - EMAIL_ADDRESS
    - PERSON
    - US_SSN
    - IBAN_CODE
    - PHONE_NUMBER
    - CREDIT_CARD
  language: en                # Extend to multilingual in future versions

policy_engine:
  max_per_call_usd: 5.00      # Prevent single-transaction wallet drain
  daily_limit_usd: 50.00      # Rolling 24h aggregate limit
  max_per_endpoint_usd: 25.00 # Per-host ceiling
  # Optional: endpoint-specific overrides
  endpoint_overrides:
    "api.medrecords.io":
      max_per_call_usd: 1.00  # Stricter limits for high-risk domains

replay_guard:
  store: memory               # Use redis for multi-process deployments
  ttl_seconds: 3600           # 1-hour deduplication window
  hmac_key_env: "X402_REPLAY_HMAC_KEY"  # Load from secrets manager

audit_log:
  output: stdout              # Forward to fluentd/SIEM in production
  include_redacted_values: false  # Never log original PII, even in debug
  chain_enabled: true         # Tamper-evident HMAC chaining
```

## 🏥 High-Risk Domain: Medical/Financial Use Cases
```yaml
# config/high-risk.yaml
pii_filter:
  mode: nlp
  min_score: 0.3              # Prioritize recall over precision for GDPR/HIPAA
  entities:
    - EMAIL_ADDRESS
    - PERSON
    - US_SSN                  # Critical for HIPAA
    - IBAN_CODE               # Critical for financial compliance
    - PHONE_NUMBER
    - CREDIT_CARD
  # Add custom recognizers for medical IDs
  custom_recognizers:
    - name: "MEDICAL_RECORD_NUMBER"
      pattern: "MRN-\d{8,10}"
      score: 0.95

policy_engine:
  max_per_call_usd: 1.00      # Stricter limits for sensitive data access
  daily_limit_usd: 10.00
  require_endpoint_whitelist: true  # Only allow pre-approved APIs
  allowed_facilitators:
    - "0xTrustedFacilitatorAddress..."

replay_guard:
  store: redis                # Persistent store for audit integrity
  ttl_seconds: 86400          # 24h window for high-value transactions

audit_log:
  output: file,/var/log/x402-audit.jsonl
  retention_days: 2555        # 7 years for HIPAA compliance
  alert_on_redaction: true    # Notify compliance team of PII detections
```

## 🚀 High-Throughput: Low-Latency Agent Swarms
```yaml
# config/high-throughput.yaml
pii_filter:
  mode: regex                 # Sacrifice PERSON detection for speed
  min_score: 0.85             # Regex scores are binary: 0.85 or 1.0
  entities:
    - EMAIL_ADDRESS           # Structural patterns only
    - US_SSN
    - IBAN_CODE
    - CREDIT_CARD
  # Skip PERSON and PHONE to avoid NLP overhead

policy_engine:
  max_per_call_usd: 0.50      # Micro-payment focused
  daily_limit_usd: 25.00
  cache_policy_decisions: true  # Reduce repeated policy evaluations

replay_guard:
  store: memory               # Fastest option; accept replay risk within TTL
  ttl_seconds: 300            # 5-minute window for high-frequency payments

audit_log:
  output: async,stdout        # Non-blocking log emission
  sample_rate: 0.1            # Log 10% of allowed requests; 100% of blocked/redacted
```

## 🔧 Environment-Specific Overrides
```bash
# .env.production
X402_FACILITATOR_ADDRESS=0xProductionContract...
X402_REPLAY_HMAC_KEY=$(aws secretsmanager get-secret-value --secret-id x402/hmac-key)
X402_AUDIT_SINK=fluentd:24224
X402_POLICY_DAILY_LIMIT=100.00  # Higher limits for production scale

# .env.staging
X402_FACILITATOR_ADDRESS=0xTestFacilitator...
X402_REPLAY_HMAC_KEY=test-key-do-not-use-in-prod
X402_AUDIT_SINK=stdout
X402_POLICY_DAILY_LIMIT=10.00   # Lower limits for testing

# .env.development
X402_FACILITATOR_ADDRESS=0xLocalMock...
X402_REPLAY_HMAC_KEY=dev-key
X402_AUDIT_SINK=console
X402_POLICY_DAILY_LIMIT=5.00
X402_PII_MIN_SCORE=0.3          # Lower threshold for testing detection
```

## 🔄 Migration Path: From Standard to Hardened Client
```python
# Step 1: Install hardened client
# pip install presidio-hardened-x402

# Step 2: Minimal code change (drop-in replacement)
# BEFORE:
# from coinbase_x402 import X402Client
# client = X402Client(facilitator_address="0x...")

# AFTER:
from presidio_hardened_x402 import HardenedX402Client
client = HardenedX402Client(
    facilitator_address="0x...",
    config_path="config/recommended.yaml"  # Load your policy
)

# Step 3: Add error handling for new exceptions
try:
    response = client.request_payment(resource_url, description, reason)
except PolicyViolationError as e:
    logger.warning(f"Payment blocked by policy: {e}")
    # Fallback logic: notify user, retry with lower-cost resource, etc.
except ReplayDetectedError as e:
    logger.error(f"Replay attempt detected: {e}")
    # Security alert: investigate potential token leakage

# Step 4: Monitor audit logs
# Forward stdout/jsonl to your observability platform
# Query for "PII_REDACTED" events to validate filter effectiveness
```

> 💡 **Pro Tip**: Start with the `recommended.yaml` config, monitor for 2 weeks, then tune `min_score` and policy limits based on your actual metadata patterns and risk tolerance.
