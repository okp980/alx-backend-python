#!/bin/bash

# Messaging App - Kubernetes Deployment Script

set -e

echo "========================================="
echo "  Messaging App - Kubernetes Deployment"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}ERROR: kubectl is not installed${NC}"
    echo "Install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

echo -e "${GREEN}✓ kubectl is installed${NC}"

# Check if Kubernetes cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}ERROR: Kubernetes cluster is not accessible${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Kubernetes cluster is accessible${NC}"
echo ""

# Prompt for Docker Hub username
read -p "Enter your Docker Hub username: " DOCKER_USERNAME
read -sp "Enter your Docker Hub password: " DOCKER_PASSWORD
echo ""

echo ""
echo "Creating secrets..."

# Create Docker Hub pull secret
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username="${DOCKER_USERNAME}" \
  --docker-password="${DOCKER_PASSWORD}" \
  --docker-email="${DOCKER_USERNAME}@users.noreply.github.com" \
  --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || echo "Secret already exists or created"

echo -e "${GREEN}✓ Docker Hub secret created${NC}"

# Prompt for application secrets
echo ""
echo "Configure application secrets:"
read -p "Database URL (default: postgresql://user:password@postgres-service:5432/messaging_db): " DATABASE_URL
DATABASE_URL=${DATABASE_URL:-postgresql://user:password@postgres-service:5432/messaging_db}

read -sp "Secret key (default: auto-generated): " SECRET_KEY
SECRET_KEY=${SECRET_KEY:-$(openssl rand -base64 32 2>/dev/null || echo "changeme-secret-key-12345")}
echo ""

read -sp "Django secret (default: auto-generated): " DJANGO_SECRET
DJANGO_SECRET=${DJANGO_SECRET:-$(openssl rand -base64 32 2>/dev/null || echo "changeme-django-secret-12345")}
echo ""

# Create application secrets
kubectl create secret generic messaging-app-secrets \
  --from-literal=database-url="${DATABASE_URL}" \
  --from-literal=secret-key="${SECRET_KEY}" \
  --from-literal=django-secret="${DJANGO_SECRET}" \
  --dry-run=client -o yaml | kubectl apply -f - 2>/dev/null || echo "Secret already exists or created"

echo -e "${GREEN}✓ Application secrets created${NC}"

# Update dep.yaml with Docker Hub username
sed -i.bak "s/YOUR_DOCKERHUB_USERNAME/${DOCKER_USERNAME}/g" dep.yaml
echo -e "${GREEN}✓ Updated dep.yaml with Docker Hub username${NC}"

# Remove backup file
rm -f dep.yaml.bak

# Apply deployment
echo ""
echo "Deploying application..."
kubectl apply -f dep.yaml

echo ""
echo -e "${GREEN}✓ Deployment created!${NC}"
echo ""

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/messaging-app --timeout=300s

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Show status
echo "Deployment status:"
kubectl get deployment messaging-app
echo ""

echo "Pods:"
kubectl get pods -l app=messaging-app
echo ""

echo "Services:"
kubectl get service messaging-app-service
echo ""

# Get external IP or instructions
EXTERNAL_IP=$(kubectl get service messaging-app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")

if [ -n "$EXTERNAL_IP" ]; then
    echo -e "${GREEN}Access your application at: http://${EXTERNAL_IP}${NC}"
else
    echo -e "${YELLOW}No external IP assigned yet. Use port-forward to access:${NC}"
    echo "kubectl port-forward service/messaging-app-service 8000:80"
    echo "Then access at: http://localhost:8000"
fi

echo ""
echo "To view logs:"
echo "kubectl logs -l app=messaging-app -f"

echo ""
echo "To check deployment status:"
echo "kubectl get deployment messaging-app"

echo ""
echo "To scale the deployment:"
echo "kubectl scale deployment messaging-app --replicas=5"

echo ""
echo -e "${GREEN}Done!${NC}"

