# Deployment Quick Start

## 📋 Overview

Use the `dep.yaml` file to deploy messaging-app to Kubernetes.

## 🚀 Quick Deployment

### Option 1: Automated Script

```bash
cd messaging_app
./deploy.sh
```

The script will:

- ✅ Ask for your Docker Hub credentials
- ✅ Create all necessary secrets
- ✅ Deploy the application
- ✅ Show you how to access it

### Option 2: Manual Deployment

#### Step 1: Create Secrets

```bash
# Docker Hub secret (for pulling images)
kubectl create secret docker-registry dockerhub-secret \
  --docker-username=YOUR_DOCKERHUB_USERNAME \
  --docker-password=YOUR_DOCKERHUB_PASSWORD

# Application secrets
kubectl create secret generic messaging-app-secrets \
  --from-literal=database-url="postgresql://user:password@postgres-service:5432/messaging_db" \
  --from-literal=secret-key="your-secret-key" \
  --from-literal=django-secret="your-django-secret"
```

#### Step 2: Update dep.yaml

Edit `dep.yaml` and replace:

```yaml
image: YOUR_DOCKERHUB_USERNAME/messaging-app:latest
```

With your Docker Hub username:

```yaml
image: yourusername/messaging-app:latest
```

#### Step 3: Deploy

```bash
kubectl apply -f dep.yaml
```

#### Step 4: Verify

```bash
# Check deployment
kubectl get deployment messaging-app

# Check pods
kubectl get pods -l app=messaging-app

# Check service
kubectl get service messaging-app-service
```

#### Step 5: Access

```bash
# Get external IP
kubectl get service messaging-app-service

# Or use port-forward
kubectl port-forward service/messaging-app-service 8000:80
# Access at: http://localhost:8000
```

## 🔍 What's Deployed

The `dep.yaml` file creates:

1. **Deployment**: 3 replicas of messaging-app
2. **Service**: LoadBalancer for external access
3. **Secrets**: Database and application credentials

## 📊 Deployment Details

- **Replicas**: 3 pods
- **Image**: `your-username/messaging-app:latest`
- **Port**: 8000
- **Resources**: 256Mi-512Mi memory, 250m-500m CPU
- **Rolling Updates**: Zero downtime

## 🎯 Access Your App

### External IP Method

```bash
# Get external IP
kubectl get service messaging-app-service

# Access at: http://EXTERNAL_IP
```

### Port Forward Method

```bash
kubectl port-forward service/messaging-app-service 8000:80
# Access at: http://localhost:8000
```

## 🔧 Common Operations

### Scale Deployment

```bash
kubectl scale deployment messaging-app --replicas=5
```

### Update Image

```bash
kubectl set image deployment/messaging-app messaging-app=YOUR_USERNAME/messaging-app:v1.1
```

### View Logs

```bash
kubectl logs -l app=messaging-app -f
```

### Delete Deployment

```bash
kubectl delete -f dep.yaml
```

## 📚 Documentation

- **`KUBERNETES_DEPLOYMENT.md`** - Complete deployment guide
- **`DEPLOYMENT_QUICKSTART.md`** - This file
- **`COMPLETE_CI_CD_SUMMARY.md`** - CI/CD overview

## 🎉 Summary

**Files**:

- `dep.yaml` - Kubernetes deployment manifest
- `deploy.sh` - Automated deployment script

**Requirements**:

- Kubernetes cluster
- Docker Hub credentials
- kubectl installed

**Deploy**:

```bash
./deploy.sh
```

---

**Your app is ready to deploy to Kubernetes!** 🚀
