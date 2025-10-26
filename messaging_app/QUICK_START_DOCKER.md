# Quick Start: Docker Build & Push with Jenkins

## ✅ What's Been Added

The Jenkins pipeline now includes Docker build and push capabilities:

1. **Dockerfile** - Creates a production-ready Docker image for the messaging app
2. **.dockerignore** - Excludes unnecessary files from Docker build
3. **Updated Jenkinsfile** - Added stages for building and pushing Docker images
4. **Documentation** - Complete setup guides

## 🚀 Quick Setup (3 Steps)

### Step 1: Update Jenkinsfile

Edit `messaging_app/Jenkinsfile` and update these two lines:

**Line 8** - Replace with your Docker Hub username:

```groovy
DOCKER_HUB_REPO = 'your_dockerhub_username/messaging-app'
```

**Line 17** - Replace with your GitHub username:

```groovy
url: 'https://github.com/your_github_username/alx-backend-python.git'
```

### Step 2: Configure Docker Hub Credentials in Jenkins

1. Go to Jenkins Dashboard
2. Click: **Manage Jenkins** → **Manage Credentials** → **(global)** → **Add Credentials**
3. Fill in:
   - **Kind**: Username with password
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password
   - **ID**: `docker-hub-credentials` (must be exactly this)
4. Click **OK**

### Step 3: Run Jenkins with Docker Access

The Jenkins container needs access to Docker. Restart it with:

```bash
# Stop current Jenkins
docker stop jenkins
docker rm jenkins

# Start with Docker socket access
docker run -d --name jenkins \
    -p 8080:8080 \
    -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    jenkins/jenkins:lts
```

## 🎯 Trigger the Pipeline

1. Open your pipeline job in Jenkins
2. Click **Build Now**
3. Watch the build progress
4. After success, find your Docker image on Docker Hub

## 📋 Pipeline Stages

Your pipeline will now execute:

1. ✅ **Checkout** - Pull code from GitHub
2. ✅ **Setup Python** - Create virtual environment
3. ✅ **Database Migration** - Run Django migrations
4. ✅ **Tests** - Run pytest with coverage
5. ✅ **Build Docker Image** - Build with build number tag
6. ✅ **Push Docker Image** - Push to Docker Hub

## 🔍 Verify Success

After the pipeline completes, verify your Docker image:

```bash
# Pull and run your image
docker pull your_dockerhub_username/messaging-app:latest
docker run -p 8000:8000 your_dockerhub_username/messaging-app:latest

# Access the app at http://localhost:8000
```

## 📚 More Information

- **Full Docker Setup**: See [DOCKER_SETUP.md](./DOCKER_SETUP.md)
- **Jenkins Quick Guide**: See [JENKINS_README.md](./JENKINS_README.md)
- **Complete Setup**: See [../../SETUP_JENKINS.md](../../SETUP_JENKINS.md)

## ⚠️ Important Notes

1. **Docker Hub Repository**: Make sure the repository exists on Docker Hub first
2. **Credentials ID**: Must be exactly `docker-hub-credentials` in Jenkins
3. **Docker Access**: Jenkins container needs Docker socket mounted
4. **GitHub URL**: Update your GitHub username in the Jenkinsfile

## 🐛 Troubleshooting

### "Docker command not found" in Jenkins

Solution: Restart Jenkins with Docker socket access (see Step 3 above)

### "Authentication failed" when pushing

Solution: Check Docker Hub credentials in Jenkins, ensure ID is `docker-hub-credentials`

### "repository does not exist"

Solution: Create the repository on Docker Hub first:

1. Go to https://hub.docker.com
2. Create repository: `messaging-app`
3. Make sure it's public or you have access

## 📊 Expected Output

After successful pipeline run:

- ✅ All tests pass
- ✅ Coverage reports generated
- ✅ Docker image built: `your_username/messaging-app:BUILD_NUMBER`
- ✅ Docker image pushed: `your_username/messaging-app:latest`
- ✅ Images available on Docker Hub

---

Ready to build and push! 🚀
