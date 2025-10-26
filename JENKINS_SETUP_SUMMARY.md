# Jenkins CI/CD Setup Summary

## Files Created/Modified

### Created Files

1. **`messaging_app/Jenkinsfile`**

   - Complete Jenkins pipeline configuration
   - Pulls code from GitHub
   - Sets up Python environment
   - Runs migrations
   - Executes pytest tests with coverage
   - Generates test and coverage reports

2. **`messaging_app/pytest.ini`**

   - Pytest configuration file
   - Sets Django settings module
   - Configures test paths

3. **`SETUP_JENKINS.md`**

   - Comprehensive setup guide
   - Step-by-step instructions
   - Troubleshooting section

4. **`install_jenkins.sh`**

   - Automated Jenkins installation script
   - Checks for existing containers
   - Provides setup instructions

5. **`messaging_app/JENKINS_README.md`**
   - Quick reference guide
   - Installation steps
   - Pipeline overview

### Modified Files

1. **`messaging_app/requirements.txt`**

   - Added pytest==8.3.4
   - Added pytest-django==4.9.0
   - Added pytest-cov==6.0.0

2. **`messaging_app/chats/tests.py`**

   - Created comprehensive test suite
   - Tests for User model
   - Tests for Conversation model
   - Tests for Message model
   - Includes pytest-specific tests

3. **`messaging_app/chats/views.py`**
   - Fixed missing import: `from django.db import models`

## Next Steps

### 1. Update Jenkinsfile

**IMPORTANT:** You must update the GitHub repository URL in `messaging_app/Jenkinsfile`:

Edit line 17:

```groovy
url: 'https://github.com/YOUR_USERNAME/alx-backend-python.git'
```

Replace `YOUR_USERNAME` with your actual GitHub username (e.g., `okpunoremmanuel`).

### 2. Start Jenkins

Run the installation script:

```bash
./install_jenkins.sh
```

Or manually:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 3. Access Jenkins Dashboard

- URL: http://localhost:8080
- Get password: `docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword`

### 4. Complete Jenkins Setup

Follow the on-screen wizard:

1. Enter the admin password
2. Install suggested plugins
3. Create an admin user (or continue as admin)
4. Save and finish

### 5. Install Required Plugins

Go to: Manage Jenkins → Plugins → Available plugins

Install these plugins:

- ✅ **Pipeline** (if not already installed)
- ✅ **ShiningPanda Plugin**
- ✅ **JUnit Plugin**
- ✅ **HTML Publisher Plugin**

### 6. Configure GitHub Credentials

1. Go to: Manage Jenkins → Credentials → (global) → Add Credentials
2. Configure:
   - **Kind**: Username with password
   - **Username**: Your GitHub username
   - **Password**: Your GitHub Personal Access Token
   - **ID**: `github-credentials`
   - **Description**: "GitHub credentials"
3. Click "OK"

**To create a GitHub Personal Access Token:**

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of private repositories)
4. Generate and copy the token
5. Use this token as the password in Jenkins credentials

### 7. Create the Pipeline Job

1. In Jenkins dashboard, click "New Item"
2. Enter name: `messaging-app-pipeline`
3. Select "Pipeline" → OK
4. Scroll to Pipeline section
5. Configure:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/alx-backend-python.git`
   - **Credentials**: Select `github-credentials`
   - **Branches to build**: `*/main`
   - **Script Path**: `messaging_app/Jenkinsfile`
6. Click "Save"

### 8. Trigger Manual Build

1. Open the pipeline job
2. Click "Build Now"
3. Click on the build number (#1) in "Build History"
4. Click "Console Output" to watch the build progress

## Testing Locally

Before pushing to GitHub, test locally:

```bash
cd messaging_app
source venv/bin/activate  # or: . venv/bin/activate
pip install -r requirements.txt
pytest chats/tests.py -v
```

## Pipeline Features

- ✅ Pulls code from GitHub
- ✅ Creates Python virtual environment
- ✅ Installs dependencies from requirements.txt
- ✅ Runs Django migrations
- ✅ Executes pytest tests
- ✅ Generates JUnit XML test reports
- ✅ Generates HTML coverage reports
- ✅ Can be triggered manually

## Project Structure

```
alx-backend-python/
├── messaging_app/
│   ├── Jenkinsfile              # ← Pipeline definition
│   ├── pytest.ini              # ← Pytest config
│   ├── JENKINS_README.md        # ← Quick reference
│   ├── requirements.txt         # ← Includes pytest
│   ├── chats/
│   │   └── tests.py            # ← Test suite
│   └── ...
├── SETUP_JENKINS.md            # ← Detailed guide
├── install_jenkins.sh          # ← Auto-install script
└── JENKINS_SETUP_SUMMARY.md   # ← This file
```

## Docker Commands Reference

```bash
# Start Jenkins
docker start jenkins

# Stop Jenkins
docker stop jenkins

# View logs
docker logs -f jenkins

# Restart Jenkins
docker restart jenkins

# Remove Jenkins (keeps data)
docker rm -f jenkins

# Remove Jenkins (deletes all data)
docker rm -f jenkins && docker volume rm jenkins_home
```

## Troubleshooting

### Issue: Port 8080 already in use

**Solution**: Change the port mapping

```bash
docker run -d --name jenkins -p 8081:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Then access Jenkins at: http://localhost:8081

### Issue: Pipeline fails at checkout

**Solution**: Check:

1. GitHub credentials are correctly configured
2. Repository URL is correct
3. GitHub Personal Access Token has `repo` scope
4. Repository is accessible (public or you have access)

### Issue: Tests fail in Jenkins

**Solution**:

1. Run tests locally first: `pytest messaging_app/chats/tests.py -v`
2. Check console output for specific error messages
3. Ensure all dependencies are in `requirements.txt`
4. Check Python version compatibility

### Issue: Module not found errors

**Solution**: Update requirements.txt

```bash
pip freeze > messaging_app/requirements.txt
```

## Success Indicators

When everything is working correctly, you should see:

1. ✅ Jenkins container running: `docker ps | grep jenkins`
2. ✅ Jenkins dashboard accessible at http://localhost:8080
3. ✅ Pipeline job created in Jenkins
4. ✅ Build succeeds with green status
5. ✅ Test reports visible in build results
6. ✅ Coverage reports visible in build results

## Additional Resources

- **Detailed Setup**: See `SETUP_JENKINS.md`
- **Quick Reference**: See `messaging_app/JENKINS_README.md`
- **Jenkins Documentation**: https://www.jenkins.io/doc/
- **Pytest Documentation**: https://docs.pytest.org/

## Summary Checklist

- [ ] Updated `messaging_app/Jenkinsfile` with your GitHub username
- [ ] Created GitHub Personal Access Token
- [ ] Started Jenkins container
- [ ] Completed initial Jenkins setup
- [ ] Installed required plugins (Pipeline, ShiningPanda, JUnit, HTML Publisher)
- [ ] Configured GitHub credentials in Jenkins
- [ ] Created pipeline job in Jenkins
- [ ] Ran a successful build

## Need Help?

1. Check the console output in Jenkins for detailed error messages
2. Review the full setup guide: `SETUP_JENKINS.md`
3. Check Jenkins logs: `docker logs jenkins`
4. Test locally first before running in Jenkins
