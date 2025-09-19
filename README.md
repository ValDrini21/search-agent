# Search Agent - ADK Deployment to Google Cloud Run

A Google ADK (Agent Development Kit) search agent deployed to Google Cloud Run for scalable, serverless AI agent hosting.

## 🚀 Why This Project?

This project demonstrates how to deploy an AI agent using Google's ADK framework to Google Cloud Run, providing:

- **Cost-effective hosting** - Pay only for actual usage
- **Automatic scaling** - Handles traffic spikes automatically
- **Serverless architecture** - No server management required
- **Easy deployment** - Simple commands to deploy and manage
- **External API access** - Accessible from anywhere via HTTP

## 🏗️ Architecture

- **Framework**: Google ADK (Agent Development Kit)
- **Deployment**: Google Cloud Run
- **Container**: Docker with Python 3.11
- **API**: FastAPI with Uvicorn server
- **Authentication**: Google Cloud IAM

## 📋 Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and authenticated
- Docker installed (for local testing)
- Python 3.11+ (for local development)
- **Windows users**: Make utility (install via `choco install make`) [Install choco first if you don't have it]

## 🛠️ Setup

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Set Environment Variables

```bash
GOOGLE_CLOUD_PROJECT="your-project-id"
GOOGLE_CLOUD_LOCATION="us-central1"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="your-api-key"
```

## 🎮 Deployment

### Deploy to Cloud Run

```bash
make deploy
```

This will:

- Build the Docker container
- Deploy to Google Cloud Run
- Provide you with the service URL

## 🔐 Authentication

This API uses JWT (JSON Web Token) authentication for secure access. **Please secure your JWT secret key.**

### Authentication Architecture

This search agent implements a **microservices authentication pattern**:

- **JWT tokens are issued by your main backend application** (e.g., your primary REST API)
- **This search agent validates those tokens** (doesn't issue new ones)
- **Both applications share the same JWT secret key** for token validation
- **This allows seamless integration** between your main app and the search agent

### Why This Approach?

This architecture is particularly useful when you have:

- **Multiple microservices** that need to share authentication
- **A main application** that handles user login/session management
- **Specialized services** (like this search agent) that need to verify user identity
- **Centralized authentication** without duplicating user management logic

**Note:** Ensure your JWT secret is the same in both applications for proper token validation.

### API Endpoints Documentation\*\* 🌐

http://localhost:8000/docs

## 🧪 Testing

This project includes a comprehensive test suite to ensure the search agent API works correctly.

1. **Create a virtual environment:**

````bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

### Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
````

1. **Start the Docker container:**

```bash
docker build -t search-agent .
docker run -p 8000:8000 search-agent
```

```bash
# Run tests
pytest tests/test_agent.py -v
```

**Note:** Always test locally before deploying to production!

## 🗑️ Cleanup

### Delete the Deployment

```bash
make delete
```

This will remove the Cloud Run service and associated resources.
