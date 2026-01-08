# Pattern: Fintech Payments Platform

## META
pattern_id: fintech_payments
category: unified
domain: fintech
keywords: [payments, fraud, ledger, pci, transactions]

---

## DOMAIN
### Intent
Secure, scalable, and compliant digital payment processing.

### Mandatory Components
- Payment API
- Payment Processing Service
- Fraud Detection Engine
- Ledger Database
- Audit Logging Service

### Optional Components
- API Gateway
- Authentication Service
- Messaging / Event Bus

---

## DOMAIN_BOUNDARIES
### Responsibility Separation
- Payment API:
  - Exposes external payment endpoints
  - Performs request validation and authorization
  - MUST NOT contain business logic

- Payment Processing Service:
  - Orchestrates transactions, settlements, and refunds
  - Coordinates fraud checks and ledger updates

- Fraud Detection Engine:
  - Analyzes transactions for anomalies
  - Produces fraud decisions asynchronously when possible

- Ledger Database:
  - Stores immutable financial records
  - Enforces strong consistency guarantees

- Audit Logging Service:
  - Records compliance and audit events
  - MUST NOT be in the synchronous transaction path

### Forbidden Responsibilities
- Payment API MUST NOT write directly to the Ledger
- Ledger Database MUST NOT perform fraud logic
- Audit Logging MUST NOT block transaction processing

---

## CORE_ARCHITECTURE
### Architecture Style
Transaction-oriented microservices with strong consistency and asynchronous auditing.

### Data Flow (Logical)
API Gateway → Payment API → Payment Processing Service  
Payment Processing Service → Fraud Detection Engine  
Payment Processing Service → Ledger Database  
Payment Processing Service -.-> Audit Logging Service  

### Event Flow (Recommended)
Payment Processing Service -.-> Payment Events  
Payment Events -.-> Fraud Detection Engine  
Payment Events -.-> Audit Logging Service  

---

## CONSISTENCY_MODEL
- Strong consistency for:
  - Ledger writes
  - Transaction state
- Eventual consistency for:
  - Audit logging
  - Monitoring and analytics

---

## CAPABILITIES
### Required
- transaction_processing
- settlement_management
- refund_processing
- fraud_detection
- ledger_recording
- audit_logging

### Optional
- idempotency
- retry_handling
- reconciliation

---

## NON_FUNCTIONAL
### Security & Compliance
- PCI-DSS compliance
- Encrypted data in transit and at rest
- Tokenization of sensitive payment data

### Scalability
- Horizontal scaling of stateless services
- Async processing for non-critical paths

### Reliability
- Idempotent transaction handling
- At-least-once event delivery

---

## DIAGRAM_HINTS
### Required Connections
API Gateway → Payment API  
Payment API → Payment Processing Service  
Payment Processing Service → Fraud Detection Engine  
Payment Processing Service → Ledger Database  
Payment Processing Service -.-> Audit Logging Service  

### Forbidden Connections
Payment API → Ledger Database  
Audit Logging Service → Payment Processing Service
