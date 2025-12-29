# Pattern: API Gateway with Microservices

## Context
- Multiple backend microservices
- External and internal consumers
- Need for centralized security and routing

## Recommended Architecture
- API Gateway as single entry point
- Independent microservices per business capability
- Service-to-service communication via REST or messaging

## Non-functional Considerations
- Rate limiting and throttling
- Authentication and authorization
- API versioning
- Observability

## Typical Components
- API Gateway
- Microservices
- Auth Provider
- Service Registry
- Monitoring
