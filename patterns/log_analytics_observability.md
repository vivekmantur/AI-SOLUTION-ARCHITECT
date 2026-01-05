# Pattern: Log Analytics & Observability Platform

## META
pattern_id: log_analytics_observability
category: unified
domain: observability
keywords: [logging, metrics, tracing, observability, alerting]

---

## DOMAIN
### Intent
Centralized collection, storage, search, and analysis of logs, metrics, and traces.

## Mandatory Components
- Log Collector
- Ingestion Pipeline
- Search Engine
- Metrics Store
- Alerting Service
- Dashboard Service

---

## CORE_ARCHITECTURE
### Architecture Style
Event-driven ingestion with indexed search and time-series storage.

### Data Flow
Applications → Log Collector  
Log Collector → Ingestion Pipeline  
Ingestion Pipeline → Search Engine  
Ingestion Pipeline → Metrics Store  
Search Engine → Dashboard Service  
Metrics Store → Dashboard Service  
Metrics Store → Alerting Service

### Scalability & Availability
Horizontally scalable ingestion and storage tiers.

### Consistency Model
Eventual consistency for logs, strong consistency for alert configurations.

---

## CAPABILITIES
### Required
- real_time_ingestion
- full_text_search
- metrics_collection
- alert_rules
- visualization

### Optional
- anomaly_detection
- long_term_archival

---

## NON_FUNCTIONAL
### Security & Compliance
- RBAC
- Secure ingestion endpoints

### Performance
- High ingestion throughput
- Low-latency queries

### Availability
- High availability
- Fault tolerance

### Observability
Self-monitoring of the observability platform

---

## DIAGRAM_HINTS
### Required Connections
Log Collector → Ingestion Pipeline  
Ingestion Pipeline → Search Engine  
Ingestion Pipeline → Metrics Store  
Search Engine → Dashboard Service  
Metrics Store → Dashboard Service  
Metrics Store → Alerting Service

### Forbidden Connections
Dashboard Service → Log Collector
