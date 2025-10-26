# Quick Start: GitHub Actions CI

## ✅ What's Been Added

Your repository now has automated CI/CD using GitHub Actions!

### Files Created

1. **`.github/workflows/ci.yml`** - GitHub Actions workflow configuration
2. **`messaging_app/settings_test.py`** - Django test settings with MySQL
3. **`GITHUB_ACTIONS_SETUP.md`** - Complete setup documentation
4. **`QUICK_START_GITHUB_ACTIONS.md`** - This quick reference

### Files Modified

1. **`requirements.txt`** - Added MySQL client (`mysqlclient`) and flake8
2. **`pytest.ini`** - Updated with test settings comment

## 🚀 How It Works

### Automatic Triggers

The CI runs automatically on:

- ✅ Every push to `main` branch
- ✅ Every push to `develop` branch
- ✅ Every pull request to `main`
- ✅ Every pull request to `develop`

### What Runs

1. **Test on Multiple Python Versions**

   - Python 3.9
   - Python 3.10
   - Python 3.11

2. **MySQL Database Setup**

   - Starts MySQL 8.0 service
   - Creates test database
   - Runs migrations

3. **Run Tests**

   - Installs dependencies
   - Executes pytest
   - Generates coverage reports

4. **Code Quality**
   - Runs flake8 linting

## 📋 First Time Setup

### 1. Commit the Files

```bash
# Navigate to messaging_app directory
cd messaging_app

# Add GitHub Actions files
git add .github/workflows/ci.yml
git add messaging_app/settings_test.py
git add requirements.txt
git add pytest.ini

# Commit
git commit -m "Add GitHub Actions CI workflow"

# Push to trigger the first run
git push origin main
```

### 2. View Results

1. Go to your GitHub repository
2. Click the **"Actions"** tab
3. You'll see the workflow running
4. Click on the workflow run to see detailed logs
5. Wait for completion - should take 3-5 minutes

## 📊 Workflow Results

After a successful run, you'll see:

### ✅ Status Icons

- Green checkmark: All tests passed
- Red X: Tests failed (check logs)
- Yellow dot: In progress

### 📁 Artifacts

Click on the workflow run → Scroll to "Artifacts" to download:

- **test-results-py3.9/3.10/3.11**: Test results in XML
- **coverage-py3.9/3.10/3.11**: Coverage reports in HTML

## 🔍 Viewing Logs

Click on any step to see detailed logs:

- ✅ Green checkmark = Success
- ❌ Red X = Failure (click to see error)
- ⏳ Yellow dot = Running

## 🛠️ Testing Locally

### Option 1: Use SQLite (Simple)

```bash
# Just run pytest with default settings
cd messaging_app
pytest chats/tests.py -v
```

### Option 2: Use MySQL (Like CI)

```bash
# Start MySQL
docker run -d \
  --name mysql-test \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=messaging_test \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=testpass \
  -p 3306:3306 \
  mysql:8.0

# Wait for MySQL
sleep 10

# Run tests
cd messaging_app
DJANGO_SETTINGS_MODULE=messaging_app.settings_test \
pytest chats/tests.py -v

# Cleanup
docker stop mysql-test && docker rm mysql-test
```

## 🎯 Workflow Breakdown

### Test Job

- **Matrix**: 3 Python versions
- **Services**: MySQL 8.0
- **Steps**:
  1. Checkout code
  2. Set up Python environment
  3. Cache dependencies
  4. Install system dependencies
  5. Install Python packages
  6. Wait for MySQL
  7. Create database
  8. Run migrations
  9. Run tests
  10. Upload artifacts

### Lint Job

- **Python**: 3.11 only
- **Steps**:
  1. Checkout code
  2. Set up Python
  3. Install flake8
  4. Run linting

## 📝 Understanding the YAML

Key sections in `.github/workflows/ci.yml`:

```yaml
on:
  push:
    branches: [main, develop] # Triggers on these branches
  pull_request:
    branches: [main, develop] # Triggers on PRs to these branches

services:
  mysql:
    image: mysql:8.0 # MySQL service for tests

strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11] # Test on these versions
```

## 🐛 Troubleshooting

### "Tests failing in CI but passing locally"

**Solution**: Make sure you're testing with the correct settings

```bash
# Test with MySQL like CI
DJANGO_SETTINGS_MODULE=messaging_app.settings_test pytest chats/tests.py -v
```

### "MySQL connection failed"

**Solution**: The workflow waits for MySQL automatically, but you can add more wait time in the YAML if needed

### "Flake8 fails"

**Solution**: Fix linting errors locally first

```bash
pip install flake8
flake8 . --max-line-length=127
```

### "Coverage not generated"

**Solution**: Ensure pytest-cov is in requirements.txt (it is!)

## 📈 Workflow Status Badge

Add to your README.md:

```markdown
[![CI](https://github.com/YOUR_USERNAME/alx-backend-python/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/alx-backend-python/actions/workflows/ci.yml)
```

Replace `YOUR_USERNAME` with your GitHub username.

## 🔒 Security

- ✅ No secrets in workflow (uses test credentials)
- ✅ Tests run in isolated containers
- ✅ Artifacts are private to your repo
- ✅ Code is not exposed to external services

## ⚙️ Customization

### Change Python Versions

Edit `.github/workflows/ci.yml`:

```yaml
python-version: [3.9, 3.10, 3.11, "3.12"] # Add 3.12
```

### Skip on Draft PRs

Add to workflow:

```yaml
on:
  pull_request:
    types: [opened, ready_for_review]
```

### Add Notifications

Add Slack/Email notifications on failure:

```yaml
- name: Notify on failure
  if: failure()
  run: |
    # Send notification
```

## 📚 Learn More

- **Full Documentation**: See [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Django Testing**: https://docs.djangoproject.com/en/stable/topics/testing/

## ✨ Summary

Your project now has:

- ✅ Automated testing on every push
- ✅ Multi-version Python support
- ✅ MySQL database testing
- ✅ Code coverage reports
- ✅ Linting checks
- ✅ Artifact storage

Just push to GitHub and watch the magic happen! 🎉
