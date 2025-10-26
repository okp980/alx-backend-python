# Jenkins CI/CD Setup for messaging_app

## Quick Start

### 1. Install and Run Jenkins

From the project root directory, run:

```bash
./install_jenkins.sh
```

Or manually:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 2. Access Jenkins

- URL: http://localhost:8080
- Get admin password: `docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword`

### 3. Install Required Plugins

Go to: Manage Jenkins → Plugins → Available plugins
Install:

- ✅ Git plugin (usually pre-installed)
- ✅ Pipeline
- ✅ ShiningPanda Plugin
- ✅ JUnit Plugin
- ✅ HTML Publisher Plugin
- ✅ Cobertura Plugin (optional, for coverage)

### 4. Configure GitHub Credentials

1. Go to: Manage Jenkins → Credentials
2. Click "Add Credentials"
3. Select: Username with password
4. Enter:
   - Username: Your GitHub username
   - Password: Your GitHub Personal Access Token
   - ID: `github-credentials`
5. Click "OK"

### 5. Create Pipeline Job

1. Click "New Item"
2. Name: `messaging-app-pipeline`
3. Select "Pipeline" → OK
4. Configure:
   - Pipeline definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/YOUR_USERNAME/alx-backend-python.git`
   - Credentials: Select `github-credentials`
   - Branch: `*/main`
   - Script Path: `messaging_app/Jenkinsfile`
5. Click "Save"

### 6. Update Jenkinsfile

**IMPORTANT:** Before running the pipeline, update the Jenkinsfile:

```bash
# Edit messaging_app/Jenkinsfile
# Replace YOUR_USERNAME with your actual GitHub username
```

Line 17:

```
url: 'https://github.com/okpunoremmanuel/alx-backend-python.git'  # Replace with your username
```

### 7. Run the Pipeline

1. Open your pipeline job
2. Click "Build Now"
3. Monitor progress by clicking the build number (#1)
4. Click "Console Output" for detailed logs

## Pipeline Stages

The Jenkins pipeline will:

1. **Checkout** - Clones code from GitHub
2. **Setup Python Environment** - Creates venv and installs dependencies
3. **Database Migration** - Runs Django migrations
4. **Tests** - Runs pytest with coverage reports
5. **Build** - Marks build as complete

## Test Reports

After a successful run, you can view:

- Test results (JUnit XML)
- Coverage reports (HTML format)
- Console output with detailed logs

## Project Structure

```
messaging_app/
├── Jenkinsfile          # Pipeline definition
├── requirements.txt     # Python dependencies (includes pytest)
├── pytest.ini          # Pytest configuration
├── manage.py           # Django management
├── chats/
│   ├── tests.py        # Test cases
│   ├── models.py
│   ├── views.py
│   └── ...
└── messaging_app/
    ├── settings.py
    └── ...
```

## Troubleshooting

### Jenkins won't start

```bash
docker logs jenkins
docker restart jenkins
```

### Port 8080 in use

Change the port mapping:

```bash
docker run -d --name jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Pipeline fails to checkout

- Verify GitHub credentials
- Check repository URL
- Ensure repository is accessible

### Tests failing

```bash
# Run tests locally first
cd messaging_app
source venv/bin/activate
pytest chats/tests.py -v
```

### Module not found errors

```bash
# Ensure requirements.txt has all dependencies
pip install -r requirements.txt
```

## Useful Commands

```bash
# View Jenkins logs
docker logs -f jenkins

# Access Jenkins shell
docker exec -it jenkins bash

# Restart Jenkins
docker restart jenkins

# Stop Jenkins
docker stop jenkins

# Start Jenkins
docker start jenkins

# Remove Jenkins (keeps data)
docker stop jenkins && docker rm jenkins

# Remove Jenkins (deletes data)
docker stop jenkins && docker rm -v jenkins && docker volume rm jenkins_home
```

## Running Tests Locally

```bash
cd messaging_app
source venv/bin/activate  # or: venv/bin/activate
pip install -r requirements.txt
pytest chats/tests.py -v
pytest chats/tests.py -v --cov=. --cov-report=html
```

## Next Steps

- Set up GitHub webhooks for automatic builds
- Configure email notifications
- Add deployment stages
- Expand test coverage
- Integrate with Slack or other tools

## References

- [Full Setup Guide](../../SETUP_JENKINS.md)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
