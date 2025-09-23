# Project settings
PROJECT_NAME = my-agentic-app
AWS_REGION   ?= us-east-1
ACCOUNT_ID   := $(shell aws sts get-caller-identity --query Account --output text)
ECR_REPO     = $(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(PROJECT_NAME)
IMAGE_TAG    = latest

# Terraform directory
TF_DIR = infra/terraform

.PHONY: build login tag push tf-init tf-apply deploy destroy clean

## Build Docker image
build:
	docker build -t $(PROJECT_NAME) -f infra/Dockerfile .

## Login to AWS ECR
login:
	aws ecr get-login-password --region $(AWS_REGION) | \
	docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

## Tag Docker image for ECR
tag:
	docker tag $(PROJECT_NAME):latest $(ECR_REPO):$(IMAGE_TAG)

## Push Docker image to ECR
push: tag
	docker push $(ECR_REPO):$(IMAGE_TAG)

## Terraform init
tf-init:
	cd $(TF_DIR) && terraform init

## Terraform apply (requires var for secrets)
tf-apply:
	cd $(TF_DIR) && terraform apply -auto-approve \
		-var="aws_region=$(AWS_REGION)" \
		-var="openai_api_key=$$OPENAI_API_KEY" \
		-var="anthropic_api_key=$$ANTHROPIC_API_KEY"

## Full deploy: build + push + terraform apply
deploy: build login push tf-init tf-apply
	@echo "✅ Deployment complete!"
	@echo "API Gateway URL:"
	cd $(TF_DIR) && terraform output api_url

## Destroy all Terraform resources
destroy:
	cd $(TF_DIR) && terraform destroy -auto-approve \
		-var="aws_region=$(AWS_REGION)" \
		-var="openai_api_key=$$OPENAI_API_KEY" \
		-var="anthropic_api_key=$$ANTHROPIC_API_KEY"

## Format terraform code
fmt:
	cd $(TF_DIR) && terraform fmt -recursive

## Validate terraform code
validate:
	cd $(TF_DIR) && terraform validate

## Clean dev artifacts (safe clean)
clean:
	docker rmi $(PROJECT_NAME):latest || true
	docker rmi $(ECR_REPO):$(IMAGE_TAG) || true

## Reset terraform state (heavy clean - optional)
reset:
	cd $(TF_DIR) && rm -rf .terraform
	cd $(TF_DIR) && rm -f .terraform.lock.hcl
