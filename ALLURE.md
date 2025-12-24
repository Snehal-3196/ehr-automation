Allure Report Generation
========================

This file contains the commands to produce an Allure report from tests, serve it locally, and archive it for CI.

Run these from the project root on macOS (bash) after activating the virtual environment:

```bash
# Activate the virtual environment
source .venv/bin/activate

# (Optional) install pytest plugin that writes Allure results
python -m pip install allure-pytest

# Run tests and save Allure results to `allure-results`
pytest --maxfail=1 --disable-warnings -q --alluredir=allure-results

# Generate a static HTML report into `allure-report` (overwrite existing)
allure generate allure-results -o allure-report --clean

# Open the generated report in your browser
allure open allure-report

# OR serve results directly (starts a temporary server and opens the report)
allure serve allure-results

# Archive the generated report directory for CI artifacts
tar -czf allure-report.tgz -C allure-report .
```

Notes:

- Verify the Allure CLI is installed and on PATH: `allure --version`.
- On macOS you can install Allure using Homebrew: `brew install allure`.
- If your test framework writes results to a different directory, adjust `--alluredir` and the paths above.

GitHub Actions: Auto-publish to GitHub Pages
================================================

A GitHub Actions workflow is included at `.github/workflows/publish_allure.yml`. This workflow automatically:

1. Runs on every push to the `main` branch (or manually via the Actions tab)
2. Installs dependencies and runs `pytest --alluredir=allure-results`
3. Generates the Allure HTML report into `allure-report`
4. Publishes the report to the `gh-pages` branch using `peaceiris/actions-gh-pages`

**Setup GitHub Pages (one-time)**:

1. Go to your GitHub repository → **Settings** → **Pages**
2. Under "Build and deployment", select:
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
3. Click **Save**

After the first workflow run completes, your report will be available at:
```
https://<your-github-username>.github.io/<repository-name>/
```

**Trigger a manual report generation**:


**Notes**:

 
 Publish to Amazon S3
 --------------------
 
 This project includes a small publish script and a GitHub Actions workflow to publish the generated `allure-report` to an S3 bucket.
 
 Local publish (manual)
 
 1. Ensure `allure-report` is generated locally (see above).
 2. Install and configure AWS CLI with credentials that have permission to write to the bucket.
 
 ```bash
 # Example: configure credentials (interactive)
 aws configure
 
 # Publish locally (script will attempt a best-effort website URL)
 ./scripts/publish_allure_s3.sh s3://mb-qa-test-reports
 ```
 
 CI publish (GitHub Actions)
 
 The workflow `.github/workflows/publish_allure_s3.yml` will run on push to `main` or can be run manually.
 It expects the following GitHub repository secrets to be set:
 
 - `AWS_ACCESS_KEY_ID`
 - `AWS_SECRET_ACCESS_KEY`
 - `AWS_REGION` (optional but recommended)
 
 When the workflow runs it will:
 - Run tests and produce `allure-results`
 - Generate the HTML report into `allure-report`
 - Sync `allure-report` to `s3://mb-qa-test-reports` using `aws s3 sync`
 
 The sync command in the workflow sets objects to public-read by default and applies a short cache-control header. Adjust the workflow if you need a different ACL or want to use CloudFront.

