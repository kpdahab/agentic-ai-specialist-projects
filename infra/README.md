This folder contains all infrastructure code for the **Agentic AI Specialist Projects** portfolio:  
- **Dockerfile** for containerizing the AWS Lambda workflow  
- **Terraform (modular)** configuration for:
  - ECR repository
  - Lambda (container image)
  - API Gateway (HTTP API)
  - DynamoDB session table
  - CloudWatch log group (with retention)
  - IAM roles/policies (Lambda exec, Bedrock policy, Secrets Manager)
- **Makefile** wrapping Docker + AWS CLI + Terraform into simple commands

------------------------------

## Prerequisites

- [Docker Desktop](https://docs.docker.com/get-started/get-docker/) installed and running  
  - macOS users: confirm installation with `docker --version`
- A valid [OpenAI API Key](https://platform.openai.com/) (and optionally Anthropic key for multi‑LLM)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with credentials
- [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) installed
- Environment variables exported for secrets before deploy:
  ```bash
  export OPENAI_API_KEY=sk-your-openai-key
  export ANTHROPIC_API_KEY=sk-your-anthropic-key


## Build the docker image
docker build -t my-agentic-app -f infra/Dockerfile .

## Run the conainer locally in foreground (Ctrl + C terminates it)
docker run -p 9000:8080 \
  -e OPENAI_API_KEY=sk-your-real-key \
  my-agentic-app

OR, run in background
docker run -d -p 9000:8080 \
  -e OPENAI_API_KEY=sk-your-real-key \
  my-agentic-app

## Test the Lambda with curl (new terminal) - expect status 200 
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"document_content": "Hello world example"}'

Note: You'll see 500 if OPENAI_API_KEY is missing

## Container Management
docker ps                   # running containers
docker ps -a                # all containers (stopped + running)
docker logs <id>            # container logs
docker stop <id>            # stop container
docker rm <id>              # remove stopped container
docker rmi my-agentic-app   # remove image

------------------------------

## Deploy to AWS with Terraform + Makefile
# Common Targets
make build      # build docker image
make login      # login to ECR
make push       # push image to ECR
make tf-plan    # terraform plan
make deploy     # build, push, terraform apply
make invoke     # curl deployed API Gateway URL
make destroy    # terraform destroy
make clean      # remove local docker artifacts
make reset      # nuke .terraform (last resort)

# One-shot Deploy
export OPENAI_API_KEY=sk-your-openai-key
export ANTHROPIC_API_KEY=sk-your-anthropic-key
make deploy

# Test Deployed API Gateway
make invoke

# Destroy Infra
make destroy

# Cleanup (local)
make clean    # remove docker images
make reset    # optional: reset terraform state/cache

------------------------------

## Architecture Diagram

```text
           +-------------------+
           | Client / curl /   |
           | Web/Mobile Client |
           +--------+----------+
                    |
                    v
           +--------+-----------+
           | API Gateway (HTTP) |
           +--------+-----------+
                    |
                    v
         +----------+-----------+
         | AWS Lambda (Docker   |
         |   Container: app.py) |
         +----------+-----------+
                    |
     +--------------+---------------+
     |                              |
     v                              v
+----+------------+          +------+-----------------+
| AWS Secrets     |          | AWS DynamoDB          |
| Manager         |          | (Session Storage)     |
|  (API Keys)     |          +-----------------------+
+-----------------+                   
     |
     v
+----+-----------------+
| LLM Providers        |
| - OpenAI (API Key)   |
| - Anthropic (API Key)|
| - Bedrock (Claude,   |
|   Titan, Mistral)    |
+----------------------+

Logs -> AWS CloudWatch (14-day retention)