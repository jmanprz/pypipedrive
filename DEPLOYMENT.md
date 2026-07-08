# Deployment Strategy for pypipedrive

## Overview

This document describes the complete deployment pipeline for releasing pypipedrive to PyPI, Read the Docs, and GitHub.

## Prerequisites

- GitHub repository: `jmanprz/pypipedrive`
- PyPI account with API token
- Read the Docs account (connected via GitHub)
- Codecov account (optional, for coverage tracking)

## Step 1: Prepare the Release

### 1.1 Update Version Numbers

Update the version in `pypipedrive/__init__.py`:

```python
__version__ = "1.0.1"
```

Also update in `setup.cfg`:

```ini
version = 1.0.1
```

### 1.2 Verify Build and Tests

```bash
# Run all tests
make test

# Build documentation (check for warnings)
make docs

# Clean build artifacts
make clean
```

### 1.3 Create Git Tag and Push to GitHub

```bash
git add .
git commit -m "Release v1.0.1"
git tag v1.0.1
git push origin main
git push origin v1.0.1
```

## Step 2: Deploy to PyPI

### 2.1 Build Distribution Packages

```bash
python -m build
```

This creates:
- `dist/pypipedrive-1.0.1-py3-none-any.whl` (wheel)
- `dist/pypipedrive-1.0.1.tar.gz` (source distribution)

### 2.2 Upload to PyPI

Run this command before uploading to make sure everything is OK:

```bash
twine check dist/*
```

Using PyPI API token (recommended over password):

Configure `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
  username = __token__
  password = pypi-[your-api-token]
```

Then simply:

```bash
twine upload dist/*
```

### 2.3 Verify on PyPI

Check: https://pypi.org/project/pypipedrive/1.0.1/

## Step 3: Publish Documentation (Read the Docs)

### 3.1 One-Time Setup

1. Go to https://readthedocs.org/
2. Sign in with GitHub account
3. Click "Import a Project"
4. Select `jmanprz/pypipedrive`
5. Confirm configuration

### 3.2 Automatic Build on Release

Read the Docs automatically detects the `v1.0.1` git tag and:
1. Clones the repository at that tag
2. Installs dependencies from `requirements-dev.txt`
3. Builds documentation using `docs/source/conf.py`
4. Publishes to `pypipedrive.readthedocs.io/en/v1.0.1/`
5. Updates main docs to point to latest stable version

**Configuration File**: `.readthedocs.yml` handles this automatically.

### 3.3 Verify Documentation

- Stable (latest) version: https://pypipedrive.readthedocs.io/
- Specific version: https://pypipedrive.readthedocs.io/en/v1.0.1/

## Step 4: Code Coverage (Codecov)

### 4.1 One-Time Setup

1. Go to https://app.codecov.io/
2. Sign in with GitHub
3. Add repository `jmanprz/pypipedrive`
4. Enable GitHub Actions integration

### 4.2 Generate Coverage Report

```bash
make coverage
```

This generates `coverage.xml` from pytest coverage data.

### 4.3 Upload to Codecov

If using GitHub Actions (recommended), add to workflow:

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    flags: unittests
```

### 4.4 Verify Coverage

Check: https://app.codecov.io/gh/jmanprz/pypipedrive

## Complete Release Checklist

- [ ] Update version in `pypipedrive/__init__.py` and `setup.cfg`
- [ ] Run `make test` (all tests pass)
- [ ] Run `make docs` (no Sphinx warnings)
- [ ] Run `make coverage` (review coverage)
- [ ] Commit and tag: `git tag v1.0.1 && git push origin main v1.0.1`
- [ ] Build: `python -m build`
- [ ] Upload to PyPI: `twine upload dist/*`
- [ ] Verify PyPI: https://pypi.org/project/pypipedrive/1.0.1/
- [ ] Verify Read the Docs (auto-builds in ~5 minutes)
- [ ] Verify Codecov (if GitHub Actions configured)

## Troubleshooting

### PyPI Upload Failed
- Check credentials/token validity
- Ensure version number doesn't already exist on PyPI
- Verify wheel and source distributions exist in `dist/`

### Read the Docs Not Building
- Check `.readthedocs.yml` syntax
- Verify `requirements-dev.txt` installs correctly
- Check build logs at https://readthedocs.org/projects/pypipedrive/builds/

### Documentation Build Fails
- Run `make docs` locally to check for Sphinx errors
- Verify all docstrings are properly formatted
- Check for missing imports or broken references

## Files Involved

- `pypipedrive/__init__.py` - Version number
- `setup.cfg` - Package metadata and version
- `.readthedocs.yml` - Read the Docs configuration
- `requirements-dev.txt` - Development and build dependencies
- `docs/source/conf.py` - Sphinx configuration
- `.github/workflows/` - CI/CD workflows (if configured)

## Notes

- **requirements-dev.txt**: Used for local development AND Read the Docs builds
  - Rename to `requirements-dev.txt` only if it becomes production requirements
  - Currently includes dev tools (pytest, sphinx, black, etc.)
  
- **GitHub Actions**: Can automate testing and coverage uploads (not required but recommended)

- **Version Pinning**: Consider pinning major versions in requirements files after stable releases
