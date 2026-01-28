# 🧠 AI Solution Architect

Generate Cloud Architecture from Business Requirements using AI

## 📋 Overview

AI Solution Architect is a production-ready, full-stack application that uses AI to automatically generate comprehensive cloud architecture designs from business and technical requirements. The system analyzes requirements, matches them with proven architectural patterns, and produces detailed solution designs including diagrams, cost estimates, and infrastructure-as-code templates.

### Key Features

- 🤖 **AI-Powered Design**: Leverages LLM to understand requirements and generate architecture
- ☁️ **Multi-Cloud Support**: Azure, AWS, and GCP
- 📊 **Visual Diagrams**: Automatic Mermaid diagram generation
- 💰 **Cost Estimation**: Per-environment cost breakdown
- 🏗️ **IaC Generation**: Terraform/Bicep code stubs
- 📡 **API Specifications**: OpenAPI/Swagger stubs
- 🎨 **Modern UI**: React with Material-UI components
- 🐳 **Docker Ready**: Production-optimized containerized deployment

## 🏗️ Architecture

### Technology Stack

**Frontend:**
- React 18
- Material-UI (MUI)
- Axios for API calls
- Mermaid for diagram rendering

**Backend:**
- FastAPI (Python 3.11)
- Pydantic for data validation
- scikit-learn for pattern matching
- ReportLab for PDF generation

**Deployment:**
- Docker multi-stage build
- Docker Compose for orchestration
- FastAPI serves both API and React static files
- Production-optimized with minimal image size

## 🚀 Quick Start (Production Deployment)

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Deploy with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Solution-Architect
   ```

2. **Build and run**
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application**
   - Application: `http://localhost:8602`
   - API Documentation: `http://localhost:8602/docs`
   - Health Check: `http://localhost:8602/health`

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

5. **Stop the application**
   ```bash
   docker-compose down
   ```

### Docker Commands

```bash
# Build the Docker image
docker build -t ai-solution-architect .

# Run the container
docker run -d -p 8602:8602 --name ai-architect ai-solution-architect

# View logs
docker logs -f ai-architect

# Stop and remove container
docker stop ai-architect && docker rm ai-architect

# Using Docker Compose (recommended)
docker-compose up -d          # Start in detached mode
docker-compose down           # Stop and remove containers
docker-compose restart        # Restart services
docker-compose ps             # View running services
```

## 📦 Docker Build Details

### Multi-Stage Build Process

The Dockerfile uses an optimized multi-stage build:

**Stage 1 - Frontend Builder (Node.js 18 Alpine):**
- Installs Node.js dependencies
- Builds React production bundle
- Optimizes and minifies assets
- Result: Optimized static files

**Stage 2 - Production (Python 3.11 Slim):**
- Minimal base image for reduced size
- Installs Python dependencies
- Copies backend code
- Copies React build from Stage 1
- Single FastAPI server serves both API and frontend

**Benefits:**
- Small image size (~500MB vs 1.5GB+)
- Fast startup time
- Production-optimized
- Single container deployment

### Build Configuration

The build process is configured via:
- `Dockerfile`: Multi-stage build definition
- `.dockerignore`: Excludes unnecessary files from build context
- `docker-compose.yml`: Orchestration and configuration

## 🔧 Configuration

### Environment Variables

Optional `.env` file for configuration:

```env
# LLM Configuration (if using external API)
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4

# Application Settings
PYTHONUNBUFFERED=1
REACT_APP_API_URL=
```

### Docker Compose Configuration

The `docker-compose.yml` includes:
- Port mapping (8602:8602)
- Volume mount for patterns directory
- Health check configuration
- Restart policy
- Network configuration

### Cloud Provider Selection

Supports three cloud providers:
- **Azure** (default)
- **AWS**
- **GCP**

Select your target cloud in the application sidebar.

## 📖 API Documentation

### Core Endpoints

#### Health Check
```http
GET /health
```
Returns backend service health status.

#### Generate Architecture Design
```http
POST /design
Content-Type: application/json

{
  "requirements": "Your business/technical requirements",
  "cloud": "azure|aws|gcp"
}
```

#### List Available Patterns
```http
GET /patterns
```
Returns all available architectural patterns.

#### Generate PDF Report
```http
POST /generate_report
```
Generates a downloadable PDF report.

### Interactive Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: `http://localhost:8602/docs`
- **ReDoc**: `http://localhost:8602/redoc`

## 🎨 User Interface

### Main Components

1. **Configuration Sidebar**
   - Cloud provider selection (Azure/AWS/GCP)


2. **Requirements Input**
   - Large text area for requirements entry
   - Pre-filled example for quick testing
   - Generate button with loading state

3. **Solution Display**
   - Normalized requirements
   - Architecture overview
   - Interactive Mermaid diagrams
   - Component breakdown with cloud services
   - Non-functional requirements
   - Technology stack recommendations
   - Cost estimates by environment
   - API specifications
   - Infrastructure-as-Code templates

## 📁 Project Structure

```
AI-Solution-Architect/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry & routes
│   ├── models.py           # Pydantic data models
│   ├── llm_client.py       # LLM integration
│   ├── patterns_store.py   # Pattern matching logic
│   ├── prompts.py          # Prompt engineering
│   └── report_generator.py # PDF generation
├── frontend/               # React frontend
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── App.js         # Main component
│   │   └── index.js       # Entry point
│   └── package.json       # Dependencies
├── patterns/              # Architecture patterns
│   └── *.md              # Pattern definitions
├── utils/                # Utility modules
│   └── embedding.py      # Embedding utilities
├── Dockerfile            # Multi-stage build
├── docker-compose.yml    # Orchestration config
├── .dockerignore         # Build exclusions
├── .gitignore           # Git exclusions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔒 Security Best Practices

### Production Checklist

- [ ] **CORS Configuration**: Update CORS settings in `backend/main.py` to restrict origins
- [ ] **Environment Variables**: Use secrets management for sensitive data
- [ ] **SSL/TLS**: Configure HTTPS with valid certificates
- [ ] **Authentication**: Implement authentication/authorization if needed
- [ ] **Rate Limiting**: Add rate limiting to prevent abuse
- [ ] **Input Validation**: Ensure all inputs are validated (already implemented via Pydantic)
- [ ] **Dependency Updates**: Regularly update dependencies for security patches
- [ ] **Logging**: Configure structured logging for monitoring
- [ ] **Monitoring**: Set up health checks and alerting
- [ ] **Backup**: Implement backup strategies for data persistence

### Security Considerations

- CORS currently allows all origins (`*`) - update for production
- No authentication by default - add as needed
- Use environment variables for API keys and secrets
- Keep Docker images updated
- Review and audit dependencies regularly

## 🚢 Production Deployment

### Cloud Platform Options

**Azure:**
- Azure Container Instances (ACI)
- Azure App Service (Containers)
- Azure Kubernetes Service (AKS)

**AWS:**
- Amazon ECS (Elastic Container Service)
- AWS Fargate
- Amazon EKS (Elastic Kubernetes Service)
- AWS App Runner

**GCP:**
- Google Cloud Run
- Google Kubernetes Engine (GKE)
- App Engine (Flexible)

**Kubernetes:**
Use the provided Dockerfile with Kubernetes manifests:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-solution-architect
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-architect
  template:
    metadata:
      labels:
        app: ai-architect
    spec:
      containers:
      - name: ai-architect
        image: ai-solution-architect:latest
        ports:
        - containerPort: 8602
```

### Scaling Considerations

- **Horizontal Scaling**: Deploy multiple container instances behind a load balancer
- **Vertical Scaling**: Increase container resources (CPU/Memory) as needed
- **Caching**: Implement Redis for pattern caching
- **Database**: Add persistent storage for user data if needed
- **CDN**: Use CDN for static assets in high-traffic scenarios

## 🔍 Monitoring & Logging

### Health Checks

The application includes a health check endpoint:
```bash
curl http://localhost:8602/health
```

Docker Compose includes automatic health checks:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 40 seconds

### Logging

View application logs:
```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f ai-architect
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent Python web framework
- React and Material-UI for frontend components
- Mermaid for diagram rendering
- Docker for containerization
- The open-source community

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs`

---

**Built with ❤️ using React, FastAPI, Docker, and AI**
