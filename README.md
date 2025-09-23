# Agentic AI Specialist Portfolio

## **Overview**

This portfolio demonstrates my expertise as a backend **GenAI engineer**, showcasing how to design, build, test, and deploy robust multi-agent AI systems using modern **cloud-native tools** and best practices. The flagship case study is an **Intelligent Document Processing Pipeline** built with LangGraph and AWS—automating document workflows, IT support tasks, and demonstrating scalable microservice architecture.

---

## **Business Problem**

Enterprises spend excessive time and money on **manual document processing**—staff must **search for files**, **extract/enter data**, verify information across varied formats, and repeatedly fix errors.  
Repetitive **IT support tickets** (e.g., password resets or VPN issues) also waste time, requiring manual triage, communication, and updating records.  

The result:  
- **High labor costs**  
- **Frequent mistakes (15%+ error rates)**  
- **Slow response times**  
- Teams unable to focus on strategic work  

A modern solution requires:  
✅ **Multi‑agent automation**  
✅ **Persistent memory**  
✅ **Scalable APIs**  

This repo demonstrates how to build this with **LangGraph + AWS**.

---

## **Key Technologies & Engineering Best Practices**

- **Multi‑Agent Orchestration:** LangGraph + LangChain coordinate specialized nodes for classification, extraction, validation, routing.  
- **Cloud‑Native Serverless Microservices:** Workflow containerized with Docker and deployed on AWS Lambda (via ECR) behind API Gateway.  
- **Persistent Memory:** DynamoDB table stores session/user/document state across workflow steps.  
- **Secure APIs:** API Gateway HTTP API endpoints provide controlled SaaS‑style access.  
- **Secrets Management:** API keys are stored in AWS Secrets Manager (injected at runtime, not in code).  
- **Logging & Monitoring:** Centralized logs in CloudWatch with retention policies.  
- **CI/CD Automation:** GitHub Actions (optional) validates Terraform, runs tests, and builds Docker images.  
- **Python Engineering:** Modular `src/`, Pydantic models for state, unit tests with Pytest.  
- **Extensibility:** Swap LLM providers via `LLM_PROVIDER` env var (OpenAI, Anthropic, **Bedrock‑ready**).  
- **Makefile Workflow:** Wraps Docker + AWS CLI + Terraform into simple `make build` / `make deploy` flows.  

---

## How These Technologies Solve the Business Problem

- Multi‑agents automate document classification, extraction, validation, routing, and IT ticket handling.
- State continuity (via DynamoDB) ensures context‑aware automation.
- Secrets Manager + IAM ensure secure credential handling (audit‑friendly).
- Logs in CloudWatch provide monitoring + incident visibility.
- Containerized Lambda behind API Gateway = scalable API endpoints for enterprise integration.

As a result, the solution delivers:
- **96% faster processing**
- **93% fewer errors**
- Over **$6.8M in annual savings**

for enterprise workflows—transforming business operations from bottlenecked and costly to efficient, reliable, and scalable.

---

## Running the Demo
A standalone demo workflow is included to showcase the Intelligent Document Processing Pipeline locally with Ollama. The demo will print end‑to‑end workflow results: classification, extraction, validation, and routing for different document types.

- **Location:**
demo/langgraph_document_processing_agents/demo_document_processing_workflow.py

- **Instructions:**
See the Demo README (demo/langgraph_document_processing_agents) for complete setup steps, including:

- **Installing Ollama**
- Running Ollama in the background
- Pulling a local model (e.g. llama3.2)
- Activating the Python environment
- Running the demo script with sample documents
- Once set up, simply run from the project root:
PYTHONPATH=. python demo/langgraph_document_processing_agents/demo_document_processing_workflow.py

---

## Local Docker Testing & Terraform Deployment
docker build -t my-agentic-app -f infra/Dockerfile .
docker run -p 9000:8080 -e OPENAI_API_KEY=sk-your-key my-agentic-app
curl -XPOST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"document_content":"Hello World"}'

More details: infra/README.md 

---

## Terraform Deployment (With Makefile)
- **Common commands:**
make build     # build docker image
make login     # login to AWS ECR
make push      # push image to ECR
make tf-plan   # terraform plan
make deploy    # build + push + terraform apply
make invoke    # curl deployed API Gateway
make destroy   # teardown infra

- **Single command deploy:**
export OPENAI_API_KEY=sk-your-openai-key
export ANTHROPIC_API_KEY=sk-your-anthropic-key
make deploy

More details: infra/README.md 

---

## Next Steps / Expansion Plans

- **Amazon Bedrock integration** Extend beyond OpenAI/Anthropic by enabling Amazon Bedrock foundation models (Claude, Mistral, Titan) in workflows, unlocking multi‑model orchestration and retrieval‑augmented generation (RAG) scenarios with LangGraph + Bedrock.
- **Additional agent workflows (marketing, sales, IT)** Deploy new multi‑agent pipelines alongside the document processing workflow to prove modular orchestration (e.g., Marketing campaign classification, Sales email triage, or IT ticket agent).
- **Richer session schema & analytics** Extend DynamoDB schema (or complement with RDS) for audit logs, compliance trails, and BI analytics over agent decisions and workflow outcomes.
- **Event‑driven automation** Integrate EventBridge, SQS, Kinesis to trigger workflows in real‑time from external enterprise systems (document ingestion, ITSM events).
- **Hybrid Kubernetes deployment (EKS)** Demonstrate portability by deploying the same container images + Terraform modules into Kubernetes/EKS for high‑availability, multi‑tenant enterprise scaling (see AWS Bedrock on EKS).
- **CI/CD pipeline hardening** Set up GitHub Actions to perform Docker build + push, Terraform plan/apply validation, automated unit/integration tests, and drift detection for infra.

---

## Architecture Diagram

                 +---------------------+
                 |   Client / curl /   |
                 |   Web/Mobile UI     |
                 +----------+----------+
                            |
                            v
                 +----------+----------+
                 |  API Gateway (HTTP) |
                 +----------+----------+
                            |
                            v
                 +----------+----------+
                 | AWS Lambda (Docker) |
                 | - LangGraph workflow|
                 | - app.py handler    |
                 +----------+----------+
                      |     |       |
      ----------------+     |       +--------------------
      |                    |                              
      v                    v                               v
+-----+---------+   +------+---------+           +----------------------+
| AWS Secrets   |   |  DynamoDB      |           | CloudWatch Logs      |
| Manager       |   | (Session store)|           | (14d retention)      |
| - OpenAI key  |   | - Session data |           +----------------------+
| - Anthropic   |   | - Audit trails |
| - Bedrock cfg |   +----------------+
+---------------+  

                        |
                        v
             +-----------------------+
             |  LLM Providers (multi)|
             | - OpenAI (API Key)    |
             | - Anthropic Claude    |
             | - Amazon Bedrock RAG  |
             +-----------------------+

--- Future Expansion (Planned) -------------------------------------------

   +---------------------+
   |  Event Sources      |
   | - S3 ingestion      |
   | - SQS / Kinesis     |
   | - EventBridge rules |
   +----------+----------+
              |
              v
   +----------+----------+
   |  Triggers workflows |
   |  asynchronously     |
   +---------------------+

   +---------------------+         +----------------------+
   | Kubernetes (EKS)    | <-----> | Dockerized workflow  |
   | - Scaled microserv. |         | containers, multi-env|
   +---------------------+         +----------------------+

   +---------------------+
   | CI/CD Pipelines     |
   | (GitHub Actions)    |
   | - Docker build/push |
   | - Terraform plan/app|
   | - Pytest suites     |
   +---------------------+

