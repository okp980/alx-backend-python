# Docker Hub Integration with GitHub Actions

## Overview

The GitHub Actions workflow now automatically builds and pushes Docker images to Docker Hub on every push to `main` or `develop` branches.

## 🚀 What's Included

### Automatic Docker Operations

When you push to `main` or `develop`:

1. ✅ Tests run (across Python 3.9, 3.10, 3.11)
2. ✅ Linting checks pass
3. ✅ **Docker image is built**
4. ✅ **Docker image is pushed to Docker Hub**

### Image Tags

Your images will be tagged as:

- `your-dockerhub-username/messaging-app:main` or `your-dockerhub-username/messaging-app:develop`
- `your-dockerhub-username/messaging-app:branch-sha` (with commit SHA)
- `your-dockerhub-username/messaging-app:latest` (only on main branch)

Example:

- `your-username/messaging-app:main-a1b2c3d4e5f6`
- `your-username/messaging-app:latest`

## 📋 Setup Instructions

### Step 1: Configure GitHub Secrets

**Important**: You must add Docker Hub credentials to GitHub Secrets.

1. **Go to your GitHub repository**
2. **Click Settings** → **Secrets and variables** → **Actions**
3. **Click "New repository secret"**
4. **Add two secrets**:

#### Secret 1: Docker Username

- **Name**: `DOCKER_USERNAME`
- **Value**: Your Docker Hub username
- **Example**: `myusername`

#### Secret 2: Docker Password

- **Name**: `DOCKER_PASSWORD`
- **Value**: Your Docker Hub password or access token
- **Example**: Your Docker Hub password or access token

**Note**: For better security, use a Docker Hub access token instead of password:

1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Name it (e.g., "GitHub Actions")
4. Copy the token and use it as `DOCKER_PASSWORD`

### Step 2: Verify Docker Secrets

Your secrets should look like this:

```
Name                  Type
─────────────────────────────────
DOCKER_USERNAME       Secret
DOCKER_PASSWORD       Secret
```

### Step 3: Push to Trigger Build

```bash
# Commit the workflow changes
git add .github/workflows/ci.yml
git commit -m "Add Docker build and push to GitHub Actions"
git push origin main
```

### Step 4: Check Workflow

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Find the workflow run
4. You should see a new job: **"Build and Push Docker Image"**

## 🔍 How It Works

### Workflow Structure

```
1. Test Job (Python 3.9, 3.10, 3.11)
   └─ Tests must pass ✅

2. Lint Job
   └─ Linting must pass ✅

3. Docker Build Job (only on push to main/develop)
   └─ Builds Docker image
   └─ Pushes to Docker Hub
```

### Conditional Execution

The Docker job only runs when:

- ✅ Push to `main` branch (not pull requests)
- ✅ Push to `develop` branch (not pull requests)
- ✅ Tests have passed
- ✅ Linting has passed

This means:

- ❌ Pull requests won't build/push images (saves resources)
- ✅ Only successful builds push images (quality control)
- ✅ Images are tagged with branch and commit SHA

## 🐳 Using Your Docker Images

### Pull and Run

After the workflow completes, pull your image:

```bash
# Login to Docker Hub
docker login

# Pull your image
docker pull your-username/messaging-app:latest

# Run the container
docker run -p 8000:8000 your-username/messaging-app:latest

# Or pull specific version
docker pull your-username/messaging-app:main
```

### Run with Environment Variables

```bash
docker run -p 8000:8000 \
  -e MYSQL_HOST=your-mysql-host \
  -e MYSQL_PORT=3306 \
  -e MYSQL_DATABASE=messaging_db \
  your-username/messaging-app:latest
```

## 📊 Monitoring Builds

### View Image Build Logs

1. Go to **Actions** tab in your repository
2. Click on a workflow run
3. Click on **"Build and Push Docker Image"** job
4. See detailed build logs

### Check Docker Hub

1. Go to https://hub.docker.com
2. Click on your repository: `your-username/messaging-app`
3. See all pushed tags
4. View build history

## 🔐 Security Best Practices

### 1. Use Access Tokens

Instead of using your Docker Hub password, create an access token:

```
https://hub.docker.com/settings/security
```

### 2. Secrets Management

- ✅ Never commit secrets to code
- ✅ Use GitHub Secrets
- ✅ Rotate tokens regularly
- ✅ Use least privilege principle

### 3. Image Security

- ✅ Scan images for vulnerabilities
- ✅ Keep base images updated
- ✅ Use specific tags, not just `latest`

## 🛠️ Troubleshooting

### Issue: "secrets.DOCKER_USERNAME not found"

**Solution**: Add the secrets to GitHub

1. Go to repository → Settings → Secrets → Actions
2. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`

### Issue: "authentication failed"

**Solution**: Check credentials

- Verify username is correct
- Use access token instead of password
- Ensure token has push permissions

### Issue: "push access denied"

**Solution**: Check Docker Hub permissions

- Ensure you're owner/collaborator on the repository
- Check token has proper scopes

### Issue: Docker job not running

**Solution**: Check conditions

- Only runs on push (not pull requests)
- Only runs on `main` or `develop` branches
- Tests and lint must pass first

## 📁 Files Modified

### `.github/workflows/ci.yml`

Added Docker build job:

```yaml
docker-build-and-push:
  name: Build and Push Docker Image
  runs-on: ubuntu-latest
  needs: [test, lint]
  if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop')
  steps:
    - name: Checkout code
    - name: Set up Docker Buildx
    - name: Log in to Docker Hub
    - name: Extract metadata
    - name: Build and push Docker image
```

## 🎯 Workflow Summary

### On Push to Main/Develop:

1. ✅ Run tests (Python 3.9, 3.10, 3.11)
2. ✅ Run linting
3. ✅ Build Docker image
4. ✅ Push to Docker Hub
5. ✅ Tag with branch and SHA

### On Pull Request:

1. ✅ Run tests
2. ✅ Run linting
3. ⏭️ Skip Docker build (saves resources)

## 🚀 Quick Commands

### Check Your Images on Docker Hub

```bash
# Search for your images
docker search your-username/messaging-app

# List local images
docker images | grep messaging-app

# Pull latest
docker pull your-username/messaging-app:latest

# Run
docker run -p 8000:8000 your-username/messaging-app:latest
```

### View GitHub Actions Logs

```bash
# Check workflow status
gh run list

# View latest run
gh run view

# Watch a running workflow
gh run watch
```

## 📝 Example Workflow Run

### Successful Build Output

```
✅ test job (Python 3.9)
✅ test job (Python 3.10)
✅ test job (Python 3.11)
✅ lint job
✅ docker-build-and-push job

Artifacts:
- Test results for Python 3.9/3.10/3.11
- Coverage reports
- Docker image: your-username/messaging-app:latest
```

## 🎓 Best Practices

### Development Workflow

1. **Make changes** to your code
2. **Test locally**: `pytest chats/tests.py -v`
3. **Lint locally**: `flake8 .`
4. **Push to branch**: `git push origin feature-branch`
5. **Create PR**: Tests and linting run
6. **Merge to main**: Docker image is built and pushed

### CI/CD Pipeline

```
Developer Push → GitHub Actions Triggers
    ↓
Run Tests (3 Python versions)
    ↓
Run Linting
    ↓
Build Docker Image (only on main/develop)
    ↓
Push to Docker Hub
    ↓
Deploy (manual or automatic)
```

## 🎉 Summary

**Your setup now includes**:

- ✅ Automatic Docker image building
- ✅ Secure credential management via GitHub Secrets
- ✅ Conditional building (only on main/develop)
- ✅ Multiple image tags for versioning
- ✅ Build caching for faster builds
- ✅ Integration with existing tests

**Result**: Fully automated CI/CD with Docker image deployment! 🐳🚀

---

## References

- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Build GitHub Action](https://github.com/docker/build-push-action)
