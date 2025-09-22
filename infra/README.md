# Infrastructure: Local Docker & Terraform

This folder contains all infrastructure code for the **Agentic AI Specialist Projects** portfolio:  
- A Dockerfile for containerizing the AWS Lambda workflow  
- Terraform configuration for deploying it into AWS Lambda with ECR  

## Prerequisites

- [Docker Desktop](https://docs.docker.com/get-started/get-docker/) installed and running  
  - macOS users: confirm installation with `docker --version`  
- A valid [OpenAI API Key](https://platform.openai.com/)  
- AWS CLI + Terraform installed if you plan to deploy to AWS

⚠️ Note: For local Docker testing, you do **not** need a `.env` file.  
Instead, pass `OPENAI_API_KEY` directly at runtime with `-e`.


## Build the docker image
docker build -t my-agentic-app -f infra/Dockerfile .

## Run the conainer locally
docker run -p 9000:8080 \
  -e OPENAI_API_KEY=sk-your-real-key \
  my-agentic-app

## Test the Lambda with curl (new terminal) - expect status 200 
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"document_content": "Hello world example"}'

# You'll see 500 if OPENAI_API_KEY is missing

## Clean up
docker ps -a
docker rm <CONTAINER_ID>
docker rmi my-agentic-app
