# RISKS — Register

> Scoring: L (1..5), I (1..5), Risk = L×I

| RiskID | Description | Link (F/NFR) | L | I | Risk | Strategy | Owner | Due | Closure Criteria |
|--------|-------------|--------------|---|---|------|----------|-------|-----|------------------|
| R1     | Error details leakage | F1, NFR-01 | 2 | 5 | 10 | Mitigate | @owner | 2025-10-20 | Contract tests passing |
| R2     | Missing security headers | API, NFR-02 | 2 | 4 | 8 | Mitigate | @owner | 2025-10-20 | Headers in 100% responses |
| R3     | Oversized request body DoS | F3, NFR-03 | 3 | 4 | 12 | Mitigate | @owner | 2025-10-25 | 413 for >1MB + tests |
| R4     | Dependency vulnerabilities | Build, NFR-04 | 3 | 5 | 15 | Mitigate | @owner | 2025-10-25 | SCA CI in place |
| R5     | Uptime below SLO | F1, NFR-05 | 2 | 4 | 8 | Transfer | @owner | 2025-10-30 | Monitoring + alerts |
| R6     | High latency under load | F1, NFR-06 | 3 | 3 | 9 | Mitigate | @owner | 2025-10-30 | Load test report p95≤150ms |
| R7     | PII in logs | API, NFR-07 | 2 | 5 | 10 | Mitigate | @owner | 2025-10-20 | Log scan CI clean |
| R8     | Burst abuse of public APIs | F1, NFR-08 | 3 | 4 | 12 | Mitigate | @owner | 2025-10-30 | e2e rate-limit test |
