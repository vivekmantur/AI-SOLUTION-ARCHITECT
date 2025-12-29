# Pattern: Multi-tenant SaaS Data Ingestion and Analytics

## Context
- Multi-tenant SaaS
- CSV / Excel uploads
- Analytics dashboards

## Recommended Architecture
- Web frontend
- API layer
- Validation and processing services
- Relational storage with tenant isolation

## Non-functional Considerations
- Tenant isolation
- Row-level security
- Scalability

## Typical Components
- Web Frontend
- API Gateway
- Ingestion Service
- Validation Service
- Analytics Engine

## Mandatory Components
- Tenant Resolver
- Ingestion Service
- Validation Service
- Analytics Engine
- Reporting Dashboard
