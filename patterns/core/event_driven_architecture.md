# Pattern: Event-Driven Architecture

## Context
- Asynchronous workflows
- Decoupled services
- High scalability requirements

## Recommended Architecture
- Event producers emit events
- Message broker or event bus
- Event consumers react independently

## Non-functional Considerations
- Event ordering
- At-least-once delivery
- Idempotency
- Back-pressure handling

## Typical Components
- Event Producers
- Message Broker
- Event Consumers
- Dead Letter Queue
