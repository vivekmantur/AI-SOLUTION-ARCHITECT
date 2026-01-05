# Pattern: Video Streaming Platform

## META
pattern_id: video_streaming_platform
category: unified
domain: media
keywords: [video, streaming, transcoding, cdn]

---

## DOMAIN
### Intent
Upload, process, and stream video content globally with low latency.

## Mandatory Components
- Video Upload Service
- Video Player Frontend
- Transcoding Pipeline
- Media Storage
- CDN
- Metadata Service

---

## CORE_ARCHITECTURE
### Architecture Style
Asynchronous media processing and global content delivery architecture.

### Data Flow
Video Player Frontend → Video Upload Service  
Video Upload Service → Media Storage  
Media Storage → Transcoding Pipeline  
Transcoding Pipeline → CDN  
Video Upload Service → Metadata Service  
Video Player Frontend → CDN  

### Scalability & Availability
Decoupled processing and delivery layers with globally distributed CDN.

### Consistency Model
Eventual consistency for media processing, strong consistency for metadata.

---

## CAPABILITIES
### Required
- video_processing
- adaptive_streaming
- content_delivery
- background_processing
- global_distribution

---

## NON_FUNCTIONAL
### Performance
- Low startup latency
- Adaptive bitrate streaming

### Scalability
- High bandwidth delivery
- Regional edge caching

---

## DIAGRAM_HINTS
### Required Connections
Video Player Frontend → Video Upload Service  
Video Upload Service → Media Storage  
Media Storage → Transcoding Pipeline  
Transcoding Pipeline → CDN  
Video Upload Service → Metadata Service  
Video Player Frontend → CDN  
