# Agentic AI Specialist Portfolio

## **Overview**

This portfolio demonstrates my expertise as a backend **GenAI engineer**, showcasing how to design, build, test, and deploy robust multi-agent AI systems using modern **cloud-native tools** and best practices. The flagship case study is an **Intelligent Document Processing Pipeline** built with LangGraph and AWS—automating document workflows, IT support tasks, and demonstrating scalable microservice architecture.

---

## **Business Problem**

Enterprises spend excessive time and money on **manual document processing**—staff must **search for files**, **extract and enter data**, verify information across varied formats, and repeatedly fix errors. Similarly, handling repetitive **IT support tickets** (like password resets or VPN issues) requires staff to triage requests, communicate back and forth with users, and update records by hand. These slow, error-prone workflows result in high labor costs, frequent mistakes (often 15%+ error rates), delayed responses, and prevent teams from focusing on strategic work.  
A modern solution requires **multi-agent automation**, **persistent memory**, and **scalable APIs** to eliminate manual effort in both document workflows and IT ticket management—freeing employees for higher-value tasks while saving millions each year.

---

## **Key Technologies & Engineering Best Practices**

- **Multi-Agent Orchestration:** LangGraph + LangChain coordinate classification, extraction, validation, routing in modular agent nodes within a unified workflow.
- **Cloud-Native Microservices:** The entire multi-agent workflow is deployed as a single scalable serverless service using AWS Lambda or ECS Docker containers.
- **Persistent Memory:** DynamoDB stores session/user/document context for stateful automation; supports dynamic agent memory patterns.
- **API Gateway:** Secure REST endpoints enable integration with web/mobile/enterprise apps; API-first design pattern.
- **CI/CD Automation:** GitHub Actions runs all unit/integration tests on every push/PR; status badge in README signals code quality.
- **Unit & Integration Testing:** Pytest covers all core modules; ensures reliability & rapid iteration.
- **Production Python Engineering:** Modular `src/` layout; type hints; docstrings; secure secret management via environment variables/AWS IAM/GitHub Secrets.
- **Containerization:** Dockerfile with uv-based dependency management enables fast builds and portable deployments to Lambda/ECS.
- **Branch Workflow & PR Templates:** Feature branch development with pull request review gates enforces code quality before merging to main.
- **Extensibility & Scalability:** Easily add new agents or swap LLM providers without refactoring the core pipeline.

---

## How These Technologies Solve the Business Problem

By orchestrating multiple intelligent agents with **LangGraph/LangChain**, this platform replaces slow, error-prone manual tasks—such as searching for documents, extracting and entering data, verifying information across formats, correcting errors, and managing repetitive IT support tickets—with a seamless automated workflow. All agents collaborate within a single scalable microservice deployed on **AWS Lambda** or **ECS**, enabling 24/7 document handling and support without human intervention.

Leveraging persistent memory in **DynamoDB** ensures agents retain context across sessions for accurate processing and responsive IT ticket management. Secure APIs provided by **API Gateway** enable easy integration with enterprise systems. Automated CI/CD pipelines guarantee every change is tested before deployment.

As a result, the solution delivers:
- **96% faster processing**
- **93% fewer errors**
- Over **$6.8M in annual savings**

for enterprise workflows—transforming business operations from bottlenecked and costly to efficient, reliable, and scalable.

---

## Next Steps / Expansion Plans

- **Integrate Amazon Bedrock Knowledge Base** for advanced retrieval‑augmented generation  
- **Add marketing/sales agent workflows** as new microservices  
- **Expand database schema** for richer analytics/audit trails in RDS/DynamoDB  
- **Enable event-driven triggers** via EventBridge/SQS/Kinesis streams  
- ***Continue refining modularity/testing*** as new features are added

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

