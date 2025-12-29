#!/bin/bash

# Check if the report directory exists
if [ ! -d "allure-report" ]; then
    echo "Error: 'allure-report' directory not found. Please run generate_allure.sh first."
    exit 1
fi

echo "Opening Allure report..."
allure open allure-report