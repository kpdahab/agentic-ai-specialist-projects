# =============================================================================
# RUN DEMO SCRIPT
# =============================================================================

1. Install Ollama
brew install ollama

- Check Installation
ollama --version

2. Run Ollama in the Background
- One-off
ollama serve

- Persistent (backgroundservice with Homebrew on macOS)
brew services start ollama

- Check
brew services list | grep ollama

- Stop service (when needed)
brew services stop ollama

3. Pull a Model
ollama pull llama3.2

- Optional (Interactive Testing)
ollama run llama3.2

4. Set up Python Environment
python3.12 -m venv .venv
On Linux/macOS: source .venv/bin/activate | On Windows: .venv\Scripts\activate
pip install -r requirements.txt

5. Verify Ollama API
curl http://localhost:11434/api/version

6. Run the Demo Script
PYTHONPATH=. python demo/langgraph_document_processing_agents/demo_document_processing_workflow.py
- Troubleshoot: if langchain-ollama not found
pip install -U langchain-ollama

# =============================================================================
# RUN ROI REPORT SCRIPT
# =============================================================================

1. PYTHONPATH=. python demo/langgraph_document_processing_agents/roi-report.py