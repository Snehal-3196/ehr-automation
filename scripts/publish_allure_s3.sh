#!/usr/bin/env bash
set -euo pipefail

# Publishes the local `allure-report` directory to the specified S3 bucket.
# Usage: ./scripts/publish_allure_s3.sh s3://mb-qa-test-reports

BUCKET_URL=${1:-}

if [ -z "$BUCKET_URL" ]; then
  echo "Usage: $0 s3://your-bucket-name"
  exit 1
fi

if [ ! -d "allure-report" ]; then
  echo "Directory 'allure-report' not found. Generate the report first (see ALLURE.md)."
  exit 1
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "AWS CLI not found. Install it and configure credentials (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)"
  exit 1
fi

if [ -z "${AWS_ACCESS_KEY_ID:-}" ] || [ -z "${AWS_SECRET_ACCESS_KEY:-}" ]; then
  echo "AWS credentials not set in environment. Export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY (and optionally AWS_REGION)."
  exit 1
fi

echo "Syncing ./allure-report -> ${BUCKET_URL} (objects will be overwritten and deleted if removed locally)"

# Sync files and set public read by default. Adjust ACL as needed for private buckets.
aws s3 sync ./allure-report "$BUCKET_URL" --delete --acl public-read \
  --cache-control "max-age=300,public"

echo "Published to ${BUCKET_URL}"

# Try to construct a website endpoint (best-effort). This assumes the bucket has website hosting enabled.
BUCKET_NAME=$(echo "$BUCKET_URL" | sed -E 's|s3://||')
REGION=$(aws s3api get-bucket-location --bucket "$BUCKET_NAME" --output text 2>/dev/null || true)
if [ -z "$REGION" ] || [ "$REGION" = "None" ]; then
  REGION="us-east-1"
fi

echo "Bucket region: $REGION"
if [ "$REGION" = "us-east-1" ]; then
  echo "Likely website URL (if website hosting enabled): http://$BUCKET_NAME.s3-website.amazonaws.com/"
else
  echo "Likely website URL (if website hosting enabled): http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com/"
fi

echo "Done."
