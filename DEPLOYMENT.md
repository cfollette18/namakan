# Namakan Deployment Guide

This guide covers deploying the Namakan platform to Azure production environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Azure Production Deployment](#azure-production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring & Observability](#monitoring--observability)
6. [Scaling Strategy](#scaling-strategy)

---

## Prerequisites

### Required Tools

- Docker Desktop
- Node.js 18+ and npm
- Python 3.11+
- Azure CLI (`az`)
- kubectl (for AKS management)
- Git

### Azure Resources

- Azure subscription with appropriate permissions
- Azure OpenAI Service access
- Resource group created

---

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-org/namakan.git
cd namakan
```

### 2. Start Infrastructure Services

**Windows:**
```bash
.\start-dev.bat
```

**Linux/Mac:**
```bash
chmod +x start-dev.sh
./start-dev.sh
```

This will:
- Start PostgreSQL with pgvector
- Start Redis
- Start Redis Commander (http://localhost:8081)
- Start pgAdmin (http://localhost:5050)
- Launch backend in terminal 1
- Launch frontend in terminal 2

### 3. Access Local Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Redis Commander**: http://localhost:8081
- **pgAdmin**: http://localhost:5050
  - Email: admin@namakan.dev
  - Password: admin123

### 4. Run Database Migrations

```bash
cd backend
prisma db push
```

---

## Azure Production Deployment

### Architecture Overview

```
Azure Front Door (CDN + WAF)
    ↓
Application Gateway (Load Balancer + SSL)
    ↓
Azure Kubernetes Service (AKS)
    ├── Frontend Pods (Next.js)
    ├── Backend Pods (FastAPI)
    └── Worker Pods (Celery)
    ↓
Data Layer:
    ├── Azure PostgreSQL Flexible Server (with pgvector)
    ├── Azure Cosmos DB (global distribution)
    ├── Azure Redis Cache (Premium tier)
    ├── Azure Blob Storage (documents, artifacts)
    └── Azure OpenAI Service (Claude/GPT models)
```

### Step 1: Set Up Azure Resources

#### 1.1 Login to Azure

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

#### 1.2 Create Resource Group

```bash
az group create \
  --name namakan-prod-rg \
  --location eastus
```

#### 1.3 Create Azure Container Registry

```bash
az acr create \
  --resource-group namakan-prod-rg \
  --name namakanacr \
  --sku Premium \
  --location eastus

# Enable admin access
az acr update --name namakanacr --admin-enabled true

# Get credentials
az acr credential show --name namakanacr
```

#### 1.4 Create AKS Cluster

```bash
az aks create \
  --resource-group namakan-prod-rg \
  --name namakan-aks \
  --node-count 3 \
  --node-vm-size Standard_D4s_v3 \
  --enable-managed-identity \
  --attach-acr namakanacr \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group namakan-prod-rg \
  --name namakan-aks
```

#### 1.5 Create PostgreSQL Database

```bash
az postgres flexible-server create \
  --resource-group namakan-prod-rg \
  --name namakan-postgres \
  --location eastus \
  --admin-user namakanadmin \
  --admin-password "YOUR_SECURE_PASSWORD" \
  --sku-name Standard_D4s_v3 \
  --tier GeneralPurpose \
  --storage-size 128 \
  --version 16

# Enable pgvector extension
az postgres flexible-server parameter set \
  --resource-group namakan-prod-rg \
  --server-name namakan-postgres \
  --name azure.extensions \
  --value VECTOR

# Create database
az postgres flexible-server db create \
  --resource-group namakan-prod-rg \
  --server-name namakan-postgres \
  --database-name namakan_prod
```

#### 1.6 Create Redis Cache

```bash
az redis create \
  --resource-group namakan-prod-rg \
  --name namakan-redis \
  --location eastus \
  --sku Premium \
  --vm-size P1 \
  --enable-non-ssl-port false
```

#### 1.7 Create Cosmos DB

```bash
az cosmosdb create \
  --resource-group namakan-prod-rg \
  --name namakan-cosmos \
  --kind GlobalDocumentDB \
  --locations regionName=eastus failoverPriority=0 \
  --default-consistency-level Session \
  --enable-automatic-failover true
```

#### 1.8 Create Storage Account

```bash
az storage account create \
  --resource-group namakan-prod-rg \
  --name namakanstorage \
  --location eastus \
  --sku Standard_GRS \
  --kind StorageV2

# Create containers
az storage container create \
  --account-name namakanstorage \
  --name documents

az storage container create \
  --account-name namakanstorage \
  --name artifacts
```

#### 1.9 Create Key Vault

```bash
az keyvault create \
  --resource-group namakan-prod-rg \
  --name namakan-keyvault \
  --location eastus \
  --enable-rbac-authorization false

# Store secrets
az keyvault secret set \
  --vault-name namakan-keyvault \
  --name postgres-password \
  --value "YOUR_POSTGRES_PASSWORD"

az keyvault secret set \
  --vault-name namakan-keyvault \
  --name openai-api-key \
  --value "YOUR_OPENAI_KEY"
```

### Step 2: Build and Push Docker Images

#### 2.1 Build Backend Image

```bash
cd backend
docker build -t namakanacr.azurecr.io/namakan-backend:latest .
docker push namakanacr.azurecr.io/namakan-backend:latest
```

#### 2.2 Build Frontend Image

```bash
cd frontend
docker build -t namakanacr.azurecr.io/namakan-frontend:latest .
docker push namakanacr.azurecr.io/namakan-frontend:latest
```

### Step 3: Deploy to Kubernetes

#### 3.1 Create Kubernetes Secrets

```bash
kubectl create secret generic namakan-secrets \
  --from-literal=postgres-password="YOUR_PASSWORD" \
  --from-literal=redis-password="YOUR_REDIS_PASSWORD" \
  --from-literal=openai-api-key="YOUR_OPENAI_KEY"
```

#### 3.2 Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/worker-deployment.yaml
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/ingress.yaml
```

#### 3.3 Verify Deployment

```bash
kubectl get pods -n namakan
kubectl get services -n namakan
kubectl logs -f deployment/namakan-backend -n namakan
```

### Step 4: Configure Application Gateway & Front Door

#### 4.1 Create Application Gateway

```bash
az network application-gateway create \
  --resource-group namakan-prod-rg \
  --name namakan-appgw \
  --location eastus \
  --sku WAF_v2 \
  --capacity 2 \
  --vnet-name namakan-vnet \
  --subnet appgw-subnet \
  --public-ip-address namakan-appgw-pip
```

#### 4.2 Create Front Door

```bash
az afd profile create \
  --resource-group namakan-prod-rg \
  --profile-name namakan-frontdoor \
  --sku Premium_AzureFrontDoor

az afd endpoint create \
  --resource-group namakan-prod-rg \
  --profile-name namakan-frontdoor \
  --endpoint-name namakan-endpoint
```

---

## Environment Configuration

### Backend Environment Variables

Create `.env` file in `backend/`:

```env
# Database
DATABASE_URL=postgresql://user:password@namakan-postgres.postgres.database.azure.com:5432/namakan_prod
COSMOS_DB_ENDPOINT=https://namakan-cosmos.documents.azure.com:443/
COSMOS_DB_KEY=your_cosmos_key

# Redis
REDIS_URL=rediss://:password@namakan-redis.redis.cache.windows.net:6380

# AI Services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
AZURE_OPENAI_ENDPOINT=https://namakan-openai.openai.azure.com/
AZURE_OPENAI_KEY=your_azure_openai_key

# Storage
AZURE_STORAGE_CONNECTION_STRING=your_connection_string

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=https://namakanai.com,https://www.namakanai.com,https://namakan.ai,https://www.namakan.ai

# Monitoring
APPLICATION_INSIGHTS_KEY=your_app_insights_key
```

### Frontend Environment Variables

Create `.env.local` in `frontend/`:

```env
NEXT_PUBLIC_API_URL=https://api.namakan.ai
NEXT_PUBLIC_WS_URL=wss://api.namakan.ai/ws
```

---

## Monitoring & Observability

### Application Insights

```bash
az monitor app-insights component create \
  --resource-group namakan-prod-rg \
  --app namakan-insights \
  --location eastus \
  --application-type web
```

### Log Analytics

```bash
az monitor log-analytics workspace create \
  --resource-group namakan-prod-rg \
  --workspace-name namakan-logs \
  --location eastus
```

### Key Metrics to Monitor

- **API Response Time**: < 200ms p95
- **Agent Task Completion Rate**: > 95%
- **Database Query Performance**: < 50ms p95
- **Redis Cache Hit Rate**: > 90%
- **Error Rate**: < 0.1%
- **Token Usage**: Track per-user and per-project

### Alerts

Set up alerts for:
- High error rates
- Slow response times
- Database connection issues
- High token usage
- Circuit breaker activations

---

## Scaling Strategy

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: namakan-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: namakan-backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Database Scaling

- **Read Replicas**: Add read replicas for heavy read workloads
- **Connection Pooling**: Use PgBouncer for connection management
- **Partitioning**: Partition large tables by project_id or date

### Redis Scaling

- **Clustering**: Enable Redis clustering for > 10GB data
- **Sharding**: Shard by user_id or project_id
- **Eviction Policy**: Use `allkeys-lru` for cache

### Cost Optimization

1. **Smart Model Routing**: Use Haiku for simple tasks, Sonnet for complex, Opus for critical
2. **Prompt Caching**: Cache common prompts in Redis (90% cache hit = 90% cost reduction)
3. **Batch Processing**: Batch similar agent tasks together
4. **Auto-scaling**: Scale down during off-peak hours
5. **Reserved Instances**: Use Azure Reserved Instances for predictable workloads

---

## Security Best Practices

1. **Network Security**
   - Use Azure Private Link for database connections
   - Enable WAF on Application Gateway
   - Implement rate limiting

2. **Authentication & Authorization**
   - Use Azure AD for SSO
   - Implement RBAC for API endpoints
   - Rotate secrets regularly

3. **Data Protection**
   - Encrypt data at rest (Azure Storage encryption)
   - Encrypt data in transit (TLS 1.3)
   - Implement data retention policies

4. **Compliance**
   - GDPR compliance for EU users
   - SOC 2 Type II certification
   - Regular security audits

---

## Backup & Disaster Recovery

### Database Backups

```bash
# Automated backups (enabled by default)
az postgres flexible-server backup create \
  --resource-group namakan-prod-rg \
  --name namakan-postgres \
  --backup-name manual-backup-$(date +%Y%m%d)
```

### Disaster Recovery Plan

1. **RPO (Recovery Point Objective)**: 1 hour
2. **RTO (Recovery Time Objective)**: 4 hours
3. **Multi-region deployment**: Primary (East US), Secondary (West US)
4. **Automated failover**: Using Azure Traffic Manager

---

## Troubleshooting

### Common Issues

**Issue: Pods not starting**
```bash
kubectl describe pod <pod-name> -n namakan
kubectl logs <pod-name> -n namakan
```

**Issue: Database connection timeout**
- Check firewall rules
- Verify connection string
- Check network security groups

**Issue: High latency**
- Check Application Insights for bottlenecks
- Review database query performance
- Check Redis cache hit rate

---

## Support

For deployment issues:
- Email: devops@namakan.ai
- Slack: #namakan-deployment
- Docs: https://docs.namakan.ai

---

**Last Updated**: January 19, 2026
