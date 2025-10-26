# Jenkins CI/CD Setup Guide

This guide will help you set up Jenkins in a Docker container and configure a CI/CD pipeline for the messaging_app project.

## Prerequisites

- Docker installed on your machine
- GitHub repository with access
- Basic knowledge of Jenkins

## Step 1: Run Jenkins in Docker Container

Execute the following command to start Jenkins:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

This command will:

- Pull the latest Long-Term Support (LTS) Jenkins image
- Expose Jenkins on port 8080
- Map the Jenkins home directory to a volume named `jenkins_home` to persist data
- Start Jenkins in detached mode

Wait for the container to start (it may take a minute or two).

## Step 2: Initial Jenkins Setup

1. Open your browser and navigate to `http://localhost:8080`
2. You'll see an "Unlock Jenkins" page. To get the initial admin password, run:

```bash
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

3. Copy the password and paste it into the Jenkins unlock page
4. Click "Continue"

## Step 3: Install Suggested Plugins

1. On the "Customize Jenkins" page, click "Install suggested plugins"
2. Wait for the installation to complete (this may take a few minutes)
3. Create your admin user or click "Continue as admin"
4. Click "Save and Finish"
5. Click "Start using Jenkins"

## Step 4: Install Required Plugins

1. From the Jenkins dashboard, click "Manage Jenkins" on the left sidebar
2. Click "Plugins"
3. Click on the "Available plugins" tab
4. Search for and install the following plugins:
   - **Git plugin** (usually pre-installed)
   - **Pipeline**
   - **ShiningPanda Plugin**
   - **JUnit Plugin** (for test reports)
   - **HTML Publisher Plugin** (for coverage reports)
   - **Cobertura Plugin** (for coverage reports)
5. After selecting the plugins, click "Install without restart"
6. Once installation is complete, click "Restart Jenkins when installation is complete"
7. Wait for Jenkins to restart

## Step 5: Configure GitHub Credentials

1. From the Jenkins dashboard, click "Manage Jenkins"
2. Click "Credentials"
3. Click the "(global)" domain
4. Click "Add Credentials"
5. Configure as follows:
   - **Kind**: SSH Username with private key (for Git SSH) OR Username with password (for HTTPS)
   - **Username**: Your GitHub username
   - **Private Key** or **Password**: Your GitHub credentials
   - **ID**: Set a memorable ID like `github-credentials`
   - **Description**: "GitHub credentials for alx-backend-python"
6. Click "OK"

### Option A: Using SSH (Recommended for private repos)

If using SSH:

- Copy your public SSH key to GitHub (Settings → SSH and GPG keys)
- Use the SSH URL format in the Jenkinsfile

### Option B: Using Personal Access Token (HTTPS)

If using HTTPS:

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Use this token as the password in Jenkins credentials

## Step 6: Create a Pipeline Job

1. From the Jenkins dashboard, click "New Item"
2. Enter an item name (e.g., "messaging-app-pipeline")
3. Select "Pipeline" as the project type
4. Click "OK"

## Step 7: Configure the Pipeline

1. Scroll down to the "Pipeline" section
2. Select "Pipeline script from SCM"
3. Configure as follows:
   - **SCM**: Git
   - **Repository URL**: Your GitHub repository URL (e.g., `https://github.com/YOUR_USERNAME/alx-backend-python.git`)
   - **Credentials**: Select the credentials you created in Step 5
   - **Branches to build**: `*/main`
   - **Script Path**: `messaging_app/Jenkinsfile`
4. Click "Save"

## Step 8: Update Jenkinsfile

Before running the pipeline, you need to update the Jenkinsfile with your GitHub username:

1. Edit `messaging_app/Jenkinsfile`
2. Replace `YOUR_USERNAME` with your actual GitHub username
3. Commit and push the changes to GitHub

Example:

```
url: 'https://github.com/okpunoremmanuel/alx-backend-python.git'
```

## Step 9: Run the Pipeline

1. From the Jenkins dashboard, click on your pipeline project
2. Click "Build Now" to trigger the pipeline manually
3. Click on the build number (#1) in the Build History to watch the progress
4. Click "Console Output" to see the detailed logs

## Understanding the Pipeline

The Jenkins pipeline performs the following stages:

1. **Checkout**: Clones the code from GitHub
2. **Setup Python Environment**: Creates a virtual environment and installs dependencies
3. **Database Migration**: Runs Django migrations
4. **Tests**: Runs pytest with coverage reports
5. **Build**: Marks the build as complete

After completion, you'll see:

- Test results in the JUnit format
- Coverage reports in HTML format
- Console output with detailed logs

## Troubleshooting

### Jenkins won't start

```bash
# Check if the container is running
docker ps -a | grep jenkins

# View logs
docker logs jenkins

# Restart the container
docker restart jenkins
```

### Port 8080 already in use

If port 8080 is already in use, you can change it:

```bash
docker run -d --name jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Then access Jenkins at `http://localhost:8081`

### Permission denied errors

```bash
# Check container logs
docker logs jenkins

# Grant permissions (if needed)
docker exec -u root -it jenkins chown -R jenkins:jenkins /var/jenkins_home
```

### Pipeline fails to checkout

- Verify your GitHub credentials in Jenkins
- Check the repository URL in the Jenkinsfile
- Ensure you have access to the repository

### Tests failing

- Check the console output for specific error messages
- Ensure all dependencies are listed in `requirements.txt`
- Run tests locally first: `pytest messaging_app/chats/tests.py -v`

## Stopping and Removing Jenkins

If you need to stop or remove Jenkins:

```bash
# Stop the container
docker stop jenkins

# Remove the container (but keep data)
docker rm jenkins

# Remove everything including data
docker volume rm jenkins_home
docker rm -v jenkins
```

## Useful Commands

```bash
# View Jenkins logs
docker logs -f jenkins

# Access Jenkins container shell
docker exec -it jenkins bash

# Check Jenkins status
docker ps | grep jenkins

# Restart Jenkins
docker restart jenkins
```

## Next Steps

- Configure webhooks to trigger builds automatically on push
- Set up email notifications for build failures
- Configure Slack or other integrations
- Add more comprehensive tests
- Set up deployment stages

## Additional Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
