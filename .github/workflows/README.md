## 📦 Release & PyPI Publishing Guide

PySantec is automatically published to PyPI using a GitHub Actions workflow triggered on tag pushes.

## 🚀 How It Works

Publishing is automated via the `Publish to PyPI` GitHub Actions workflow.

### 🔁 Trigger Conditions

The workflow runs when either:

- A Git tag matching the pattern `v*.*.*` is pushed to the repository (e.g., `v0.1.0`)
- A manual trigger is initiated via GitHub UI (`workflow_dispatch`)

### 📋 Steps Performed

The release workflow consists of two jobs:

1. 🛠️ `build`

- Checks out the repository
- Sets up Python (`3.x`)
- Installs packaging tools: `build` and `twine`
- Builds the Python package using `python -m build`
- Uploads the built `.whl` and `.tar.gz` files as artifacts

2. 📤 `publish` (requires `build` to finish)

- Downloads the build artifacts
- Publishes them to PyPI using `gh-action-pypi-publish`

---

### 🔐 Secrets & Auth

To authenticate with PyPI, the workflow uses an API token stored as a GitHub secret:

- Name: `PYPI_API_TOKEN`
- Create the token from your PyPI account: https://pypi.org/manage/account/token/
- Set the token in your repository under:
  `Settings > Secrets and variables > Actions > New repository secret`

### 🧪 Optional: Test on TestPyPI

To test publishing without affecting the real PyPI, modify the `publish` step by uncommenting this line:

```yaml
repository_url: https://test.pypi.org/legacy/
```

Then push a tag like `v0.1.0-rc1` to test without releasing a stable version.

---

### 🏁 How to Publish a New Release

1. Update version in `pyproject.toml` (e.g., `version = "0.1.0"`)
2. Commit and push changes to `main` (or merge a feature PR)
3. Create and push a new Git tag:

    ```bash
    git tag v0.1.0
    git push origin v0.1.0
    ```

4. GitHub Actions will handle:

- Building the package
- Publishing it to PyPI

---

### 📂 Distribution Files

The following files are built and published:

- `dist/pysantec-<version>.tar.gz` (source archive)
- `dist/pysantec-<version>-py3-none-any.whl` (wheel)

---

### 🧩 Notes

* Ensure all dependencies are declared in `pyproject.toml`
* Keep changelogs and versioning consistent before tagging
* Tagging should only be done after all tests pass

---

### 📎 Example

To publish version `0.1.0`:
    
```bash
# Update version
vi pyproject.toml
 
# Commit changes
git commit -am "Release v0.1.0"

# Tag and push
git tag v0.1.0
git push origin v0.1.0
```

### 🎉 Your package will be available on PyPI in minutes.
