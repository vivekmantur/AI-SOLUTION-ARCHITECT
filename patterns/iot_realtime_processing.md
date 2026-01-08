# Pattern: IoT Real-Time Processing

## META
pattern_id: iot_realtime_processing
category: unified
domain: iot
keywords: [telemetry, streaming, realtime, monitoring]

---

## DOMAIN
### Intent
Real-time telemetry ingestion, processing, and monitoring.

## Mandatory Components
- IoT Ingestion Gateway
- Stream Processor
- Time-Series Store
- Alerting Service
- Dashboard Service

---

## CORE_ARCHITECTURE
### Architecture Style
Event-driven streaming architecture.

### Data Flow
IoT Ingestion Gateway → Stream Processor  
Stream Processor → Time-Series Store  
Stream Processor → Alerting Service  
Time-Series Store → Dashboard Service

---

## CAPABILITIES
### Required
- streaming_ingestion
- realtime_processing
- alerting
- monitoring

---

## NON_FUNCTIONAL
### Performance
- Low latency
- High throughput

### Scalability
- Global scale
- Horizontal scaling

### Availability
- High availability
- Fault tolerance

---

## DIAGRAM_HINTS
### Required Connections
IoT Ingestion Gateway → Stream Processor  
Stream Processor → Time-Series Store  
Stream Processor → Alerting Service  
Time-Series Store → Dashboard Service
