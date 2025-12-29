#!/bin/bash
set -e

# Check if Allure is installed
if ! command -v allure &> /dev/null; then
    echo "Error: 'allure' command not found."
    echo "Please install it (e.g., 'brew install allure')."
    exit 1
fi

# Check if results exist
if [ ! -d "allure-results" ]; then
    echo "Warning: 'allure-results' directory not found. Make sure you ran tests with '--alluredir=allure-results'."
fi

echo "Generating Allure report..."
allure generate allure-results -o allure-report --clean

echo "Opening Allure report..."
allure open allure-report