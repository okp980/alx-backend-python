# Linting and Coverage Setup

## Overview

The GitHub Actions workflow has been enhanced to include:

- ✅ **Strict flake8 linting** - Fails build on any linting errors
- ✅ **Code coverage reports** - Comprehensive coverage tracking
- ✅ **Build artifacts** - Upload and retention of coverage data
- ✅ **Summary reports** - Visual summaries in workflow logs

## What Was Added

### 1. Enhanced Linting (Flake8)

**Location**: `.github/workflows/ci.yml` → `lint` job

**Features**:

- ✅ Fails the build if any linting errors are detected
- ✅ Uses `.flake8` configuration file
- ✅ Excludes venv, migrations, and other unnecessary files
- ✅ Shows detailed error messages with source code
- ✅ Generates summary in workflow logs

**Configuration File**: `.flake8`

```ini
max-line-length = 127
max-complexity = 10
exclude = .git,__pycache__,venv,env,.venv,migrations
select = E9,F63,F7,F82,W,F
```

### 2. Enhanced Coverage Reports

**Location**: `.github/workflows/ci.yml` → `test` job

**Features**:

- ✅ Uploads both HTML and XML coverage reports
- ✅ 30-day retention period for artifacts
- ✅ Coverage summary in workflow logs
- ✅ Separate artifacts for each Python version

**Artifacts**:

- `coverage-report-py3.9` - Coverage for Python 3.9
- `coverage-report-py3.10` - Coverage for Python 3.10
- `coverage-report-py3.11` - Coverage for Python 3.11

## How It Works

### Linting Job

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Install linting tools
        run: pip install flake8

      - name: Run flake8 linting
        id: flake8
        run: |
          flake8 . --count --statistics

      - name: Linting summary
        run: |
          echo "## Linting Results" >> $GITHUB_STEP_SUMMARY
          # Shows pass/fail status
```

**Result**:

- ✅ Build passes if no linting errors
- ❌ Build fails if any linting errors found

### Coverage Reports

```yaml
- name: Upload coverage reports
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report-py${{ matrix.python-version }}
    path: |
      htmlcov/
      coverage.xml
    retention-days: 30

- name: Coverage summary
  run: |
    echo "## Coverage Report" >> $GITHUB_STEP_SUMMARY
```

**Result**: Artifacts available for 30 days with coverage data

## Running Locally

### Run Linting

```bash
cd messaging_app

# Install flake8
pip install flake8

# Run linting
flake8 . --count --statistics

# Or use the config file (automatically reads .flake8)
flake8 .
```

### Run Coverage Tests

```bash
cd messaging_app

# Run tests with coverage
pytest chats/tests.py -v --cov=. --cov-report=html --cov-report=xml

# View HTML report
open htmlcov/index.html

# View XML report (for CI)
cat coverage.xml
```

## Linting Rules

### Error Codes Checked

- **E9**: SyntaxError, IndentationError
- **F63**: print statements (should use logging)
- **F7**: Syntax errors
- **F82**: Undefined names
- **W**: Warnings
- **F**: PyFlakes checks

### Ignored

- **Line length**: Up to 127 characters (configurable)
- **Complexity**: Up to 10 (configurable)
- **Settings/migrations**: Excluded files

### Excluded Files

- `.git/`, `__pycache__/`, `venv/`, `env/`
- `migrations/`
- `*.egg-info/`
- `dist/`, `build/`

## Viewing Results

### In GitHub

1. **Go to Actions tab**
2. **Click on a workflow run**
3. **View results**:
   - Lint job: Shows if linting passed/failed
   - Test job: Shows coverage for each Python version
4. **Download artifacts**:
   - Click on "Artifacts" at the top
   - Download coverage reports as zip files

### Local Coverage Report

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html
```

## Configuration Files

### `.flake8`

```ini
[flake8]
max-line-length = 127
max-complexity = 10
exclude = .git,__pycache__,venv,migrations
select = E9,F63,F7,F82,W,F
ignore = W503
```

### `pytest.ini`

```ini
[pytest]
DJANGO_SETTINGS_MODULE = messaging_app.settings_test
testpaths = chats
python_files = tests.py test_*.py *_tests.py
```

## Troubleshooting

### Linting Errors

**Error**: `E501: line too long`

**Solution**: Break long lines:

```python
# Bad
result = function_call(param1, param2, param3, param4, param5, param6)

# Good
result = function_call(
    param1, param2, param3,
    param4, param5, param6
)
```

**Error**: `F401: module imported but unused`

**Solution**: Remove unused imports or add `# noqa: F401`

**Error**: `F821: undefined name 'undefined_var'`

**Solution**: Fix the undefined variable

### Coverage Not Generated

**Check**:

1. pytest-cov is installed: `pip install pytest-cov`
2. Running with coverage flag: `pytest --cov=.`
3. Coverage files are not gitignored

**Fix**:

```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
```

## Best Practices

### Before Committing

1. **Run linting**:

   ```bash
   flake8 .
   ```

2. **Fix errors** (if any)

3. **Run tests with coverage**:

   ```bash
   pytest --cov=. --cov-report=html
   ```

4. **Check coverage report**

5. **Commit and push**

### IDE Integration

**VS Code**:

- Install Python extension
- Install flake8 extension
- Settings: `"python.linting.flake8Enabled": true`

**PyCharm**:

- Configure flake8 in preferences
- Enable on-save inspections

## Workflow Summary

### Successful Build

When all checks pass, you'll see:

- ✅ Lint job: "All linting checks passed!"
- ✅ Test jobs: Coverage reports uploaded
- ✅ Build status: Green checkmark

### Failed Build

When errors are found:

- ❌ Lint job: Shows specific errors
- ❌ Test job: Shows which tests failed
- ❌ Build status: Red X with error details

## Next Steps

1. **Monitor linting**: Keep code quality high
2. **Increase coverage**: Aim for >80% coverage
3. **Fix issues**: Address any linting errors
4. **Download reports**: Use artifacts for analysis
5. **Set up badges**: Add status badges to README

## References

- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Coverage](https://pytest-cov.readthedocs.io/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Your project now has comprehensive linting and coverage tracking! 🎉**
