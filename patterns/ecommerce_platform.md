# Pattern: E-commerce Platform

## META
pattern_id: ecommerce_platform
category: unified
domain: commerce
keywords: [catalog, cart, orders, payments, inventory]

---

## DOMAIN
### Intent
Online commerce with ordering and payments.

## Mandatory Components
- Catalog Service
- Cart Service
- Order Service
- Payment Service
- Inventory Service

### Mandatory Capabilities
- browsing
- cart_management
- order_processing
- payment_processing

### Domain Boundaries
- Order Service handles order lifecycle only
- Inventory Service exclusively manages stock levels

---

## CORE_ARCHITECTURE
### Architecture Style
Microservices with event-driven communication.

### Data Flow
Order → Payment → Inventory → Confirmation

### Scalability & Availability
Horizontal scaling, async events.

---

## CAPABILITIES
### Required
- authentication
- caching
- messaging

---

## NON_FUNCTIONAL
### Security
- PCI-DSS
- Secure payment handling

### Performance
Traffic spike handling

---

## DIAGRAM_HINTS
### Required Connections
API Gateway → Catalog Service  
API Gateway → Cart Service  
API Gateway → Order Service  
Order Service → Payment Service  
Payment Service → Inventory Service
