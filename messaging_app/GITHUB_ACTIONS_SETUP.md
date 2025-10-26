# GitHub Actions CI/CD Setup Guide

## Overview

This project uses GitHub Actions for continuous integration. The workflow runs automatically on every push and pull request to the main and develop branches.

## Workflow Configuration

The CI workflow is defined in `.github/workflows/ci.yml` and performs the following tasks:

### What the CI Does

1. **Test Matrix** - Runs tests on Python 3.9, 3.10, and 3.11
2. **MySQL Database** - Sets up MySQL 8.0 service for database tests
3. **Dependencies** - Installs all project dependencies
4. **Migrations** - Runs Django database migrations
5. **Tests** - Executes pytest with coverage reporting
6. **Linting** - Runs flake8 for code quality checks
7. **Reports** - Publishes test results and coverage reports

## Workflow Triggers

The CI runs automatically on:

- ✅ Every push to `main` branch
- ✅ Every push to `develop` branch
- ✅ Every pull request to `main` branch
- ✅ Every pull request to `develop` branch

## Workflow Structure

### Jobs

#### 1. Test Job

- **Runs on**: Ubuntu Latest
- **Python Versions**: 3.9, 3.10, 3.11 (matrix strategy)
- **Services**: MySQL 8.0
- **Steps**:
  - Checkout code
  - Set up Python environment
  - Cache pip packages
  - Install system dependencies (MySQL client)
  - Install Python dependencies
  - Set up test environment variables
  - Wait for MySQL service
  - Run Django migrations
  - Run pytest with coverage
  - Upload test results and coverage reports

#### 2. Lint Job

- **Runs on**: Ubuntu Latest
- **Python Version**: 3.11
- **Steps**:
  - Checkout code
  - Set up Python
  - Install flake8
  - Run flake8 linting

## Database Configuration

The CI uses MySQL instead of SQLite for testing. The test configuration is in `messaging_app/settings_test.py`.

### Environment Variables

```bash
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=messaging_test
MYSQL_USER=testuser
MYSQL_PASSWORD=testpass
```

### MySQL Service Configuration

The workflow automatically starts a MySQL container with:

- Database: `messaging_test`
- User: `testuser`
- Password: `testpass`
- Health checks enabled

## Viewing Results

### In GitHub

1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. Select a workflow run
4. Click on a job to see detailed logs

### Artifacts

The workflow generates and stores these artifacts:

- **test-results-pyX.X**: Test results in JUnit XML format
- **coverage-pyX.X**: Coverage reports in HTML format

To download artifacts:

1. Go to the workflow run
2. Scroll down to "Artifacts"
3. Download the zip files

## Running Tests Locally

### With MySQL (Like CI)

```bash
# Start MySQL with Docker
docker run -d \
  --name mysql-test \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=messaging_test \
  -e MYSQL_USER=testuser \
  -e MYSQL_PASSWORD=testpass \
  -p 3306:3306 \
  mysql:8.0

# Wait for MySQL to be ready
sleep 10

# Run tests
DJANGO_SETTINGS_MODULE=messaging_app.settings_test \
MYSQL_HOST=127.0.0.1 \
MYSQL_PORT=3306 \
MYSQL_DATABASE=messaging_test \
MYSQL_USER=testuser \
MYSQL_PASSWORD=testpass \
pytest chats/tests.py -v

# Clean up
docker stop mysql-test
docker rm mysql-test
```

### With SQLite (Development)

```bash
# Run tests with default settings
pytest chats/tests.py -v

# Or with coverage
pytest chats/tests.py -v --cov=. --cov-report=html
```

## Workflow Status Badge

Add a status badge to your README:

```markdown
[![CI](https://github.com/your-username/alx-backend-python/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/alx-backend-python/actions/workflows/ci.yml)
```

Replace `your-username` with your GitHub username.

## Customization

### Add More Python Versions

Edit `.github/workflows/ci.yml`:

```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11, "3.12"]
```

### Change MySQL Version

Edit the services section:

```yaml
services:
  mysql:
    image: mysql:5.7 # Change version here
```

### Skip Workflow on Draft PRs

Add to workflow:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
```

### Add More Steps

You can add additional steps to the workflow:

```yaml
- name: Build Docker Image
  run: docker build -t messaging-app .

- name: Security Scan
  run: pip install bandit && bandit -r .

- name: Type Checking
  run: pip install mypy && mypy .
```

## Troubleshooting

### Tests Fail in CI But Pass Locally

**Solution**: Check database configuration

- Ensure `settings_test.py` is using MySQL
- Verify MySQL service is running in CI
- Check environment variables are set correctly

### MySQL Connection Failed

**Solution**: Add wait step before migrations

```yaml
- name: Wait for MySQL
  run: |
    while ! mysqladmin ping -h 127.0.0.1; do
      sleep 1
    done
```

### Flake8 Fails in CI

**Solution**: Fix linting errors locally first

```bash
pip install flake8
flake8 . --max-line-length=127
```

### Coverage Reports Not Generated

**Solution**: Ensure pytest-cov is installed

- Check `requirements.txt` includes `pytest-cov==6.0.0`
- Verify coverage.xml is being generated

## Best Practices

1. **Keep tests fast** - Limit integration tests in CI
2. **Fail fast** - Add linting before expensive tests
3. **Use matrix for compatibility** - Test multiple Python versions
4. **Cache dependencies** - Speed up workflow runs
5. **Clean up resources** - Use services for databases
6. **Publish reports** - Always generate artifacts
7. **Set environment variables** - Don't hardcode values
8. **Use secrets** - Store sensitive data securely

## Security

### GitHub Secrets

For sensitive data, use GitHub Secrets:

1. Go to: Repository Settings → Secrets and variables → Actions
2. Add secret with name and value
3. Use in workflow:
   ```yaml
   env:
     SECRET_KEY: ${{ secrets.SECRET_KEY }}
   ```

## Advanced Features

### Conditional Steps

```yaml
- name: Deploy on main
  if: github.ref == 'refs/heads/main'
  run: |
    echo "Deploying to production"
```

### Matrix Strategy

Test on multiple configurations:

```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11]
    database: [sqlite, mysql, postgresql]
```

### Caching

```yaml
- name: Cache Python packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax)

## Summary

✅ **Automatic CI** - Runs on every push and PR  
✅ **Multi-Python** - Tests on Python 3.9, 3.10, 3.11  
✅ **MySQL Database** - Real database testing  
✅ **Coverage Reports** - Track test coverage  
✅ **Artifacts** - Download test results  
✅ **Linting** - Code quality checks

Your Django project now has comprehensive CI/CD! 🚀
