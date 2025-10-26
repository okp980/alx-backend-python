# Quick Start: Docker with GitHub Actions

## ✅ What's New

Your GitHub Actions workflow now automatically:

- Builds Docker images
- Pushes to Docker Hub
- Tags images with branch and SHA

## 🚀 Setup (3 Steps)

### Step 1: Add GitHub Secrets

Go to: Repository → Settings → Secrets and variables → Actions

Add two secrets:

**Secret 1:**

- Name: `DOCKER_USERNAME`
- Value: Your Docker Hub username

**Secret 2:**

- Name: `DOCKER_PASSWORD`
- Value: Your Docker Hub password or access token

### Step 2: Push to Trigger

```bash
git add .github/workflows/ci.yml
git commit -m "Add Docker build to CI"
git push origin main
```

### Step 3: Check Results

1. Go to GitHub → Actions tab
2. Watch the workflow run
3. See Docker image build and push
4. Check Docker Hub for your image

## 🎯 Workflow Behavior

### On Push to Main/Develop:

1. ✅ Run tests
2. ✅ Run linting
3. ✅ **Build Docker image**
4. ✅ **Push to Docker Hub**

### On Pull Request:

1. ✅ Run tests
2. ✅ Run linting
3. ⏭️ Skip Docker (saves resources)

## 🐳 Using Your Image

```bash
# Pull latest
docker pull your-username/messaging-app:latest

# Run
docker run -p 8000:8000 your-username/messaging-app:latest
```

## 📊 Image Tags

Each push creates multiple tags:

- `your-username/messaging-app:latest` (main branch only)
- `your-username/messaging-app:main-abc123` (with commit SHA)
- `your-username/messaging-app:develop-abc123`

## 🔍 View Results

### GitHub Actions

- Go to Actions tab
- Click workflow run
- See "Build and Push Docker Image" job

### Docker Hub

- Go to hub.docker.com
- Find `your-username/messaging-app`
- See all tags and versions

## ❓ Troubleshooting

### "Secrets not found"

- Add `DOCKER_USERNAME` and `DOCKER_PASSWORD` to GitHub Secrets

### "Authentication failed"

- Check username is correct
- Use access token instead of password

### Docker job not running

- Only runs on push (not PR)
- Must be on main or develop branches
- Tests and lint must pass first

## 📚 Full Documentation

- See `DOCKER_HUB_SETUP.md` for complete guide
- See `GITHUB_ACTIONS_SETUP.md` for CI overview

---

**Your CI/CD now includes Docker!** 🐳🚀
