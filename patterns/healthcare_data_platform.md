# Pattern: Healthcare Data Platform

## META
pattern_id: healthcare_data_platform
category: unified
domain: healthcare
keywords: [healthcare, hipaa, gdpr, encryption, audit]

---

## DOMAIN
### Intent
Sensitive healthcare data management for hospitals and research teams.

## Mandatory Components
- Secure Ingestion Service
- Encrypted Storage
- RBAC Service
- Audit Logging Service

---

## CORE_ARCHITECTURE
### Architecture Style
Secure multi-tenant, service-oriented architecture.

### Data Flow
Secure Ingestion Service → Encrypted Storage  
RBAC Service → Secure Ingestion Service  
RBAC Service → Encrypted Storage  
Encrypted Storage → Audit Logging Service

### Consistency Model
Strong consistency for patient records and access logs.

---

## CAPABILITIES
### Required
- secure_ingestion
- encryption
- access_control
- auditing

---

## NON_FUNCTIONAL
### Security & Compliance
- HIPAA
- GDPR
- Encryption at rest and in transit
- Audit logging

### Availability
- High availability
- Fault tolerance

---

## DIAGRAM_HINTS
### Required Connections
Secure Ingestion Service → Encrypted Storage  
RBAC Service → Secure Ingestion Service  
RBAC Service → Encrypted Storage  
Encrypted Storage → Audit Logging Service
