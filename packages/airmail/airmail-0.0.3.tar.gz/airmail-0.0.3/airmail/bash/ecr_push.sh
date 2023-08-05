#!/bin/bash

set -e

printf "\n"
echo "Building to repo: $ECR_REPO"
echo "Building version: $VERSION"
printf "\n"

# Grab the project dir
PROJECT_ROOT_DIR=$(pwd)
# Login to ECR
$(aws ecr get-login --no-include-email)
# Build Image
docker build -t "$ECR_REPO:$VERSION" "$PROJECT_ROOT_DIR/$APP_DIR/"
# Tag image for ECR
docker tag ${ECR_REPO}:${VERSION} ${TASK_IMAGE_TAG}
# Push to ECR
docker push ${TASK_IMAGE_TAG}
