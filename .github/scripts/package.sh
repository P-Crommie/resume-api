#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Docker image and ECR repository details
VERSION="$1"
IMAGE_NAME="cloud-resume-api"
AWS_ACCOUNT_ID="522986700920"
AWS_REGION="eu-west-1"
ECR_REPO="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_NAME}"

# Check if version argument is provided
if [ -z "$VERSION" ]; then
    echo "Error: Version argument is missing. Please provide a version tag."
    exit 1
fi

# Build the Docker image
echo "Building Docker image ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" -f ./app/Dockerfile ./app

# Tag the Docker image
echo "Tagging Docker image ${IMAGE_NAME}:latest to ${ECR_REPO}:${VERSION}..."
docker tag "${IMAGE_NAME}:latest" "${ECR_REPO}:${VERSION}"

# Push the Docker image to ECR
echo "Pushing Docker image to ${ECR_REPO}:${VERSION}..."
docker push "${ECR_REPO}:${VERSION}"

echo "Docker image pushed to ${ECR_REPO}:${VERSION} successfully."
