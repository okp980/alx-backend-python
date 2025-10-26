# Kubernetes Deployment Guide

## Overview

This guide shows how to deploy the messaging-app to Kubernetes using the `dep.yaml` file.

## 📋 Prerequisites

- Kubernetes cluster running
- `kubectl` installed and configured
- Docker Hub credentials
- PostgreSQL database (or compatible)

## 🚀 Quick Deployment

### Step 1: Configure Secrets

#### 1. Create Application Secrets

```bash
# Create the secrets file
kubectl create secret generic messaging-app-secrets \
  --from-literal=database-url="postgresql://user:password@postgres-service:5432/messaging_db" \
  --from-literal=secret-key="your-secret-key-here" \
  --from-literal=django-secret="your-django-secret-key"

# Or edit secrets via file
kubectl create -f secrets-config.yaml
```

#### 2. Create Docker Hub Pull Secret

```bash
# Create Docker Hub secret for pulling images
kubectl create secret docker-registry dockerhub-secret \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=YOUR_DOCKERHUB_USERNAME \
  --docker-password=YOUR_DOCKERHUB_PASSWORD \
  --docker-email=YOUR_EMAIL
```

### Step 2: Update dep.yaml

Edit `dep.yaml` and replace placeholders:

```yaml
image: YOUR_DOCKERHUB_USERNAME/messaging-app:latest
```

With your actual Docker Hub username:

```yaml
image: yourusername/messaging-app:latest
```

### Step 3: Deploy

```bash
# Apply the deployment
kubectl apply -f dep.yaml

# Check deployment status
kubectl get deployments

# Check pods
kubectl get pods

# Check services
kubectl get services
```

## 🔍 Verification

### Check Pods

```bash
kubectl get pods -l app=messaging-app
```

Expected output:

```
NAME                              READY   STATUS    RESTARTS   AGE
messaging-app-xxxxx-xxxxx          1/1     Running   0          1m
```

### Check Logs

```bash
# Get pod name
POD_NAME=$(kubectl get pods -l app=messaging-app -o jsonpath='{.items[0].metadata.name}')

# View logs
kubectl logs $POD_NAME

# Follow logs
kubectl logs -f $POD_NAME
```

### Check Service

```bash
kubectl get service messaging-app-service
```

## 🌐 Accessing the Application

### Get External IP

```bash
kubectl get service messaging-app-service
```

### Port Forward (Alternative)

```bash
# Forward local port 8000 to service
kubectl port-forward service/messaging-app-service 8000:80
```

Then access at: http://localhost:8000

## 📊 Deployment Details

### What Gets Deployed

1. **Deployment**: 3 replicas of messaging-app
2. **Service**: LoadBalancer type for external access
3. **Secrets**: Application and database credentials
4. **Image Pull Secret**: For Docker Hub authentication

### Resource Limits

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Health Checks

**Liveness Probe**: Checks if container is alive

```yaml
livenessProbe:
  httpGet:
    path: /health/
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

**Readiness Probe**: Checks if container is ready

```yaml
readinessProbe:
  httpGet:
    path: /health/
    port: 8000
  initialDelaySeconds: 15
  periodSeconds: 5
```

## 🔧 Configuration

### Environment Variables

Edit in `dep.yaml`:

```yaml
env:
  - name: DEBUG
    value: "False"
  - name: ALLOWED_HOSTS
    value: "messaging-app.example.com"
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: messaging-app-secrets
        key: database-url
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment messaging-app --replicas=5

# Check scaling
kubectl get deployment messaging-app
```

### Rolling Updates

Deployment uses RollingUpdate strategy:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
```

This means:

- ✅ Zero downtime updates
- ✅ Gradual rollout
- ✅ Automatic rollback on failure

## 🔐 Security

### Secrets Management

**Don't commit secrets!** Use Kubernetes secrets:

```bash
# Create secret
kubectl create secret generic messaging-app-secrets \
  --from-literal=secret-key="your-secret"
```

### Image Pull Secrets

Required for private Docker Hub repositories:

```yaml
imagePullSecrets:
  - name: dockerhub-secret
```

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# Check events
kubectl get events

# Check logs
kubectl logs <pod-name>
```

### Image Pull Errors

```bash
# Verify Docker Hub secret
kubectl get secret dockerhub-secret

# Test image pull
kubectl run test --image=YOUR_DOCKERHUB_USERNAME/messaging-app:latest
```

### Database Connection Issues

```bash
# Check if database URL is correct
kubectl get secret messaging-app-secrets -o yaml

# Test database connection
kubectl exec -it <pod-name> -- python manage.py dbshell
```

## 📈 Monitoring

### Check Deployment Status

```bash
kubectl get deployment messaging-app

# Detailed status
kubectl describe deployment messaging-app
```

### View Replicas

```bash
kubectl get rs -l app=messaging-app
```

### Pod Health

```bash
# Check pod conditions
kubectl get pods -l app=messaging-app -o wide

# Describe specific pod
kubectl describe pod <pod-name>
```

## 🔄 Updates

### Update Image

```bash
# Set new image
kubectl set image deployment/messaging-app messaging-app=YOUR_DOCKERHUB_USERNAME/messaging-app:v1.1

# Check rollout status
kubectl rollout status deployment/messaging-app

# View rollout history
kubectl rollout history deployment/messaging-app

# Rollback if needed
kubectl rollout undo deployment/messaging-app
```

### Update Config

```bash
# Edit deployment
kubectl edit deployment messaging-app

# Or apply new config
kubectl apply -f dep.yaml
```

## 🗑️ Cleanup

### Delete Resources

```bash
# Delete deployment and service
kubectl delete -f dep.yaml

# Delete secrets
kubectl delete secret messaging-app-secrets
kubectl delete secret dockerhub-secret
```

## 📝 Complete Setup

### 1. Configure Secrets

```bash
# Application secrets
kubectl create secret generic messaging-app-secrets \
  --from-literal=database-url="postgresql://user:pass@postgres:5432/db" \
  --from-literal=secret-key="super-secret-key"

# Docker Hub secret
kubectl create secret docker-registry dockerhub-secret \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD
```

### 2. Update dep.yaml

Replace `YOUR_DOCKERHUB_USERNAME` with your username

### 3. Deploy

```bash
kubectl apply -f dep.yaml
```

### 4. Verify

```bash
kubectl get all -l app=messaging-app
```

### 5. Access

```bash
# Get external IP
kubectl get service messaging-app-service

# Or port forward
kubectl port-forward service/messaging-app-service 8000:80
```

## 🎯 Best Practices

1. ✅ Use secrets for sensitive data
2. ✅ Set resource limits
3. ✅ Enable health checks
4. ✅ Use rolling updates
5. ✅ Monitor pod health
6. ✅ Keep images updated
7. ✅ Test in staging first

## 📚 References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Deploying Django to Kubernetes](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

---

**Your Django app is now ready for Kubernetes deployment!** 🚀
