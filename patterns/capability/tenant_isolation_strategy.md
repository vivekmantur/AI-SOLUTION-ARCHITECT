# Pattern: Tenant Isolation Strategy

## Context
- Multi-tenant SaaS

## Recommended Architecture
- Shared DB with tenant_id
- Row-level security

## Non-functional Considerations
- Data leakage prevention

## Typical Components
- Tenant Resolver
- Policy Engine
- Shared Database
