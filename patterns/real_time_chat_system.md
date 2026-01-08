# Pattern: Real-Time Chat System

## META
pattern_id: real_time_chat_system
category: unified
domain: messaging
keywords: [chat, websocket, realtime, presence]

---

## DOMAIN
### Intent
Low-latency real-time messaging between users with presence awareness.

## Mandatory Components
- WebSocket Gateway
- Messaging Service
- Presence Service
- Message Store
- Notification Service

---

## CORE_ARCHITECTURE
### Architecture Style
Event-driven real-time messaging architecture.

### Data Flow
Client → WebSocket Gateway  
WebSocket Gateway → Messaging Service  
Messaging Service → Message Store  
Messaging Service → Presence Service  
Presence Service → Notification Service  
Messaging Service → Notification Service

### Scalability & Availability
Horizontally scalable WebSocket gateways with stateless messaging services.

### Consistency Model
Eventual consistency for message delivery, strong consistency for presence state.

---

## CAPABILITIES
### Required
- real_time_messaging
- presence_tracking
- message_delivery
- connection_management
- fanout_delivery

---

## NON_FUNCTIONAL
### Performance
- Low latency
- High concurrency

### Reliability
- Graceful reconnect handling
- At-least-once message delivery

---

## DIAGRAM_HINTS
### Required Connections
Client → WebSocket Gateway  
WebSocket Gateway → Messaging Service  
Messaging Service → Message Store  
Messaging Service → Presence Service  
Presence Service → Notification Service  
Messaging Service → Notification Service
