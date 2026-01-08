# Pattern: Data Warehouse & Analytics Platform

## META
pattern_id: data_warehouse_analytics
category: unified
domain: analytics
keywords: [etl, data_lake, warehouse, bi, reporting]

---

## DOMAIN
### Intent
Enterprise analytics and historical reporting.

## Mandatory Components
- Data Ingestion Service
- ETL Pipeline
- Data Lake
- Data Warehouse
- BI Dashboard Service

### Mandatory Capabilities
- batch_ingestion
- transformation
- historical_analysis

---

## CORE_ARCHITECTURE
### Architecture Style
Batch-oriented analytics architecture.

### Data Flow
Sources → Ingestion → Data Lake → ETL → Warehouse → BI

### Scalability & Availability
Separation of storage and compute.

### Consistency Model
Strong consistency for warehouse queries.

---

## CAPABILITIES
### Required
- schema_management
- reporting
- cost_optimization

---

## NON_FUNCTIONAL
### Security
- Row-level security
- Data encryption
- Data Accuracy
- Cost Optimization
    

### Performance
- Optimized query execution

---

## DIAGRAM_HINTS
### Required Connections
Ingestion → Data Lake  
Data Lake → ETL Pipeline  
ETL Pipeline → Data Warehouse  
Data Warehouse → BI Dashboard
