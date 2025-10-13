# STRIDE — Threats and Controls

| Flow/Element | Threat (S/T/R/I/D/E) | Description | Control | NFR Link | Evidence/Test |
|--------------|----------------------|-------------|---------|----------|---------------|
| F1           | S (Spoofing)         | Client identity spoofing at edge | Rate limiting, auth hardening | NFR-08 | e2e negative tests |
| F1           | I (Information Disclosure) | Leak via error details | Error envelope masking | NFR-01 | tests/test_errors.py |
| F1           | E (Elevation of Privilege) | Abuse of endpoints burst | Basic rate limiting | NFR-08 | e2e burst test |
| F3           | R (Repudiation)      | Inconsistent errors impede audit | Standardized error codes | NFR-01 | contract tests |
| F3           | T (Tampering)        | Oversized bodies crash parsers | Body size limit | NFR-03 | integration test |
| F2           | I (Info Disclosure)  | OpenAPI exposes internals | Hide PII, no secrets | NFR-07 | manual review |
| F4           | D (DoS)              | Memory exhaustion by many objects | Size limits + cleanup | NFR-03 | soak test plan |
| API          | I (Info Disclosure)  | Missing security headers | Set default headers | NFR-02 | tests/test_errors.py |
