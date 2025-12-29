#!/bin/bash
set -e

# Configuration
REPO_URL="https://github.com/Snehal-3196/ehr-automation.git"
PUBLISH_BRANCH="gh-pages"
REPORT_DIR="allure-report"

# Check if report exists
if [ ! -d "$REPORT_DIR" ]; then
    echo "Error: Directory '$REPORT_DIR' not found."
    echo "Please run 'generate_allure.sh' first."
    exit 1
fi

echo "Publishing '$REPORT_DIR' to $REPO_URL on branch '$PUBLISH_BRANCH'..."

# Navigate to report directory
cd "$REPORT_DIR"

# Initialize temporary git repo for deployment
git init
git checkout -b "$PUBLISH_BRANCH"

# Add all files and commit
git add .
git commit -m "Manual publish of Allure Report: $(date)"

# Force push to the remote branch (overwrites previous report history)
git push -f "$REPO_URL" "$PUBLISH_BRANCH"

echo "✅ Published successfully!"
echo "View at: https://Snehal-3196.github.io/ehr-automation/"