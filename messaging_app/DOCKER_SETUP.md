# Docker Build and Push Setup Guide

## Overview

The Jenkins pipeline now includes stages for building and pushing Docker images to Docker Hub.

## New Pipeline Stages

1. **Checkout** - Pulls code from GitHub
2. **Setup Python Environment** - Sets up Python virtual environment
3. **Database Migration** - Runs Django migrations
4. **Tests** - Runs pytest tests
5. **Build Docker Image** - Builds Docker image with build number tag
6. **Push Docker Image** - Pushes image to Docker Hub

## Setup Instructions

### 1. Update Jenkinsfile

Edit `messaging_app/Jenkinsfile` and update the following:

**Line 8**: Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username:

```groovy
DOCKER_HUB_REPO = 'your_dockerhub_username/messaging-app'
```

**Line 14**: Replace `YOUR_USERNAME` with your GitHub username:

```groovy
url: 'https://github.com/your_github_username/alx-backend-python.git'
```

### 2. Create Docker Hub Credentials in Jenkins

1. Go to Jenkins Dashboard
2. Navigate to: **Manage Jenkins** → **Manage Credentials**
3. Select **Stores scoped to Jenkins** → **(global)**
4. Click **Add Credentials**
5. Configure as follows:
   - **Kind**: Username with password
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password or access token
   - **ID**: `docker-hub-credentials`
   - **Description**: "Docker Hub credentials"
6. Click **OK**

### 3. Update GitHub Credentials (if not already done)

1. Go to: **Manage Jenkins** → **Credentials**
2. Add or update GitHub credentials with ID: `github-credentials`

### 4. Enable Docker in Jenkins

The Jenkins server needs to be able to run Docker commands. Verify that Docker is available:

```bash
# SSH into Jenkins container
docker exec -it jenkins bash

# Check if Docker is available
docker --version

# If not available, the Jenkins container needs to be run with Docker socket mounted
```

### 5. Run Jenkins with Docker Socket Access (If Needed)

If the Jenkins container cannot run Docker commands, restart it with Docker socket access:

```bash
# Stop current Jenkins
docker stop jenkins
docker rm jenkins

# Start Jenkins with Docker socket mounted
docker run -d --name jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /usr/bin/docker:/usr/bin/docker \
    jenkins/jenkins:lts

# Or add Jenkins user to docker group (if on Linux host)
```

### 6. Install Docker Plugin (Optional)

For easier Docker integration, install the Docker Pipeline plugin:

1. Go to: **Manage Jenkins** → **Plugins**
2. Search for: **Docker Pipeline**
3. Install and restart Jenkins

## Pipeline Execution

### Trigger the Pipeline

1. Go to your pipeline job in Jenkins
2. Click **Build Now**
3. Monitor the build in real-time by clicking on the build number

### Expected Output

The pipeline will:

- ✅ Checkout code from GitHub
- ✅ Set up Python environment
- ✅ Run database migrations
- ✅ Execute pytest tests
- ✅ Build Docker image: `your_username/messaging-app:BUILD_NUMBER`
- ✅ Build Docker image: `your_username/messaging-app:latest`
- ✅ Push both tags to Docker Hub
- ✅ Clean up local images

### Verify Docker Images

After successful build, verify the images on Docker Hub:

```bash
# Login to Docker Hub
docker login

# Pull and run the image
docker run -p 8000:8000 your_username/messaging-app:latest

# Or pull specific build
docker run -p 8000:8000 your_username/messaging-app:1
```

## Docker Image Details

### Image Structure

- **Base Image**: Python 3.9-slim
- **Working Directory**: /app
- **Port**: 8000
- **Django**: Automatically runs migrations on container start
- **Command**: Runs Django development server

### Image Tags

- `your_username/messaging-app:BUILD_NUMBER` - Tagged with Jenkins build number
- `your_username/messaging-app:latest` - Always points to the latest build

## Troubleshooting

### Issue: Docker command not found

**Solution**: The Jenkins container doesn't have access to Docker daemon.

Run Jenkins with Docker socket mounted (see Step 5 above).

### Issue: Authentication to Docker Hub failed

**Solution**:

1. Verify Docker Hub credentials in Jenkins
2. Ensure credentials ID is exactly `docker-hub-credentials`
3. Test login manually:
   ```bash
   docker login
   ```

### Issue: Push failed - repository does not exist

**Solution**: Create the repository on Docker Hub first:

1. Go to https://hub.docker.com
2. Create a new repository: `messaging-app`
3. Use format: `your_username/messaging-app`

### Issue: Build failed - Dockerfile not found

**Solution**: Ensure the Dockerfile is in the messaging_app directory:

```
messaging_app/
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── ...
```

### Issue: Permission denied to socket

**Solution**: The Jenkins user needs access to Docker socket:

On Linux host:

```bash
sudo usermod -aG docker jenkins
```

Or restart Jenkins container with proper Docker socket mapping.

## Configuration Variables

You can customize these in the Jenkinsfile environment section:

```groovy
environment {
    PYTHON_VERSION = '3.9'
    DOCKER_IMAGE = 'messaging-app'
    DOCKER_TAG = "${BUILD_NUMBER}"
    DOCKER_HUB_REPO = 'your_dockerhub_username/messaging-app'
}
```

## Advanced Configuration

### Using Docker Compose

If you need to run multiple services, create a `docker-compose.yml`:

```yaml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    volumes:
      - .:/app
```

### Using Production WSGI Server

Update the Dockerfile to use Gunicorn instead of the development server:

```dockerfile
# Install Gunicorn
RUN pip install gunicorn

# Use Gunicorn instead
CMD gunicorn messaging_app.wsgi:application --bind 0.0.0.0:8000
```

## Security Notes

1. **Never commit Docker Hub credentials** to version control
2. Use **access tokens** instead of passwords when possible
3. Enable **2FA** on your Docker Hub account
4. Use **private repositories** for production images
5. Regularly **rotate credentials** in Jenkins

## Next Steps

- Configure automatic deployments to staging/production
- Set up notifications (email, Slack) for build status
- Add Docker image scanning for vulnerabilities
- Implement blue-green deployments
- Configure load balancer for production

## References

- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Jenkins Docker Plugin](https://plugins.jenkins.io/docker-plugin/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
