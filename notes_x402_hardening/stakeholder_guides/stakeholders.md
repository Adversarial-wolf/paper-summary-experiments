# Stakeholder Guides

## 🎯 For Executives (The "So What?")
**Bottom Line:** AI agents paying for services automatically create a massive, invisible privacy leak. They send customer names and emails to third-party payment servers and facilitators in plaintext.

**Business Risk:** 
- **Regulatory Fines:** Direct violation of GDPR data minimization principles.
- **Financial Loss:** Without spending caps, a malicious server could theoretically "drain" an agent's wallet via inflated prices.

**Solution:** The `presidio-hardened-x402` middleware acts as a "security firewall" for agent payments. It scrubs PII and caps spending *before* any money or data leaves your environment. It adds negligible latency (~6ms) while significantly reducing legal and financial exposure.

---

## ⚖️ For Compliance Officers (The GDPR Perspective)
**The Compliance Gap:** Under GDPR Art. 5(1)(c), personal data must be limited to what is necessary. x402 metadata (URLs, reasons) often contains PII that is *not* necessary for the financial settlement of a micropayment.

**Technical Controls Implemented:**
- **Pre-Transmission Filtering:** Redaction happens *before* the data reaches the facilitator API (a potential third-party processor).
- **Data Minimization:** Replaces PII with placeholders (e.g., `<EMAIL_ADDRESS>`), ensuring the facilitator only sees what is needed for the transaction.
- **Auditability:** The HMAC-chained log provides an immutable record of exactly what was redacted and why, supporting "Privacy by Design" documentation.

**Residual Risk:** The "PERSON" recall ceiling (~55% in URLs) means not all names are caught in URL paths. Manual review of high-risk endpoints is still recommended.

---

## 🧬 For Data Scientists & Engineers (The Implementation)
**Core Architecture:** A Python wrapper around the Coinbase x402 client.

**Key Metrics to Watch:**
- **Latency:** NLP mode p99 is ~5.73ms. If your budget is < 10ms, you are safe.
- **Precision/Recall Tradeoff:** The recommended `min_score=0.4` favors recall (blocking more) over precision.
- **The "PERSON" Problem:** If you are using URLs as primary identifiers (slugs), the standard spaCy NER model will fail. You may need to:
    1. Pre-process URLs to split slugs by delimiters (`-`, `_`).
    2. Fine-tune a model on x402-style metadata.

**Configuration Recommendation:**
- **Mode:** `nlp` (Crucial for `PERSON` and `PHONE` detection).
- **Entity Set:** All six types (`EMAIL`, `PERSON`, `PHONE`, `SSN`, `IBAN`, `CC`).
- **Threshold:** `min_score=0.4`.
